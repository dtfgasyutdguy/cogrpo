#!/usr/bin/env python
"""Train CO-GRPO.
Usage (single GPU):
    python scripts/train.py --model configs/models/qwen.yaml --epoch 1
Usage (4-GPU DDP):
    accelerate launch --multi_gpu --num_processes=4 scripts/train.py --model configs/models/qwen.yaml --epoch 1
"""
from __future__ import annotations

import argparse, json, logging, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from accelerate import Accelerator
from datasets import Dataset
from peft import LoraConfig, PeftModel, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import GRPOConfig, GRPOTrainer

from cogrpo.CO_CR import compute_rewards
from cogrpo.utils import ensure_dir, jsonl_iter, load_yaml

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")

def load_pairs(pairs_file: str):
    return list(jsonl_iter(pairs_file))

def build_dataset(records, tokenizer):
    rows = {"prompt": [], "q_co_file_text": [], "sample_id": [], "cwe_str": [], "completion_line_co": [], "co_position": []}
    for r in records:
        with open(r["q_co_file"], "r", encoding="utf-8") as fh:
            file_text = fh.read()
        rows["prompt"].append([{"role": "user", "content": r["q_co_user"]}])
        rows["q_co_file_text"].append(file_text)
        rows["sample_id"].append(r["sample_id"])
        rows["cwe_str"].append(r["cwe_str"])
        rows["completion_line_co"].append(r["completion_line_co"])
        rows["co_position"].append(r["co_position"])
    return Dataset.from_dict(rows)

def make_reward_fn(cfg, tokenizer, rank: int, cocr_reference=None):
    rank_tmp = Path(cfg["paths"]["tmp_dir"]) / f"rank{rank}"
    rank_db = Path(cfg["paths"]["codeql_dbs_dir"]) / f"rank{rank}"
    codeql_bin = cfg["paths"]["codeql_bin"]
    codeql_suite = cfg["paths"]["codeql_suite"]
    reward_cfg = cfg["reward"]

    def reward_fn(prompts, completions, completion_ids=None, sample_id=None, cwe_str=None, completion_line_co=None, q_co_file_text=None, co_position=None, **_unused):
        completion_strs = [c[0]["content"] if isinstance(c, list) and c and isinstance(c[0], dict) else c for c in completions]
        metas = [{"sample_id": sample_id[i], "cwe_str": cwe_str[i], "completion_line_co": completion_line_co[i], "q_co_file_text": q_co_file_text[i], "co_position": co_position[i]} for i in range(len(completion_strs))]
        return compute_rewards(completions=completion_strs, metas=metas, rank_tmp_dir=rank_tmp, rank_db_dir=rank_db, codeql_bin=codeql_bin, codeql_suite=codeql_suite, reward_cfg=reward_cfg, tokenizer=tokenizer, cocr_reference=cocr_reference)

    return reward_fn

def get_max_prompt_length(records, tokenizer) -> int:
    return max((len(tokenizer.apply_chat_template([{"role": "user", "content": r["q_co_user"]}], add_generation_prompt=True)) for r in records), default=0)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--epoch", type=int, required=True)
    p.add_argument("--max_steps", type=int, default=-1)
    args = p.parse_args()
    setup_logging()

    accelerator = Accelerator()
    rank = accelerator.local_process_index
    local_rank = rank

    cfg = load_yaml("configs/base.yaml")
    model_cfg = load_yaml(args.model)
    cfg = {**cfg, "model": model_cfg}

    short_name = model_cfg["short_name"]
    paths = cfg["paths"]
    pairs_file = paths["pairs_file"]
    save_root = Path(paths["checkpoints_dir"]) / f"{short_name}__co_cr"

    logger.info("Model: %s, Epoch: %d, Rank: %d", short_name, args.epoch, rank)

    records = load_pairs(pairs_file)
    logger.info("Training on %d paired records (epoch=%d)", len(records), args.epoch)

    model_path = model_cfg["model_path"]
    tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    max_prompt_len = get_max_prompt_length(records, tokenizer) + 4
    logger.info("max_prompt_length = %d", max_prompt_len)

    dataset = build_dataset(records, tokenizer)

    qcfg = cfg["quantization"]
    bnb = BitsAndBytesConfig(load_in_4bit=qcfg["load_in_4bit"], bnb_4bit_quant_type=qcfg["bnb_4bit_quant_type"], bnb_4bit_use_double_quant=qcfg["bnb_4bit_use_double_quant"], bnb_4bit_compute_dtype=getattr(torch, qcfg["bnb_4bit_compute_dtype"]))

    model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=bnb, trust_remote_code=True, dtype=getattr(torch, qcfg["bnb_4bit_compute_dtype"]), use_cache=False, device_map={"": local_rank})
    model = prepare_model_for_kbit_training(model)

    final_save = save_root / f"epoch{args.epoch}"
    if args.epoch == 2:
        prev = save_root / "epoch1"
        if prev.exists() and (prev / "adapter_config.json").exists():
            logger.info("Loading epoch1 adapter from %s", prev)
            model = PeftModel.from_pretrained(model, prev, is_trainable=True)
        else:
            raise FileNotFoundError(f"epoch1 adapter not found at {prev}")
    else:
        lcfg = cfg["lora"]
        peft_cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, inference_mode=False, r=lcfg["rank"], lora_alpha=lcfg["alpha"], lora_dropout=lcfg["dropout"], target_modules=lcfg["target_modules"])
        model = get_peft_model(model, peft_cfg)

    bs = model_cfg["batch_size_per_device"]
    opt = cfg["optimization"]
    grpo_cfg_dict = cfg["grpo"]

    grpo_args = GRPOConfig(output_dir=str(save_root), per_device_train_batch_size=bs, gradient_accumulation_steps=opt["gradient_accumulation_steps"], learning_rate=opt["learning_rate"], lr_scheduler_type=opt["lr_scheduler_type"], num_train_epochs=opt["num_train_epochs"], logging_steps=1, save_strategy="no", seed=opt["seed"], fp16=opt["fp16"], gradient_checkpointing=opt["gradient_checkpointing"], ddp_find_unused_parameters=False, remove_unused_columns=False, max_prompt_length=max_prompt_len, max_completion_length=grpo_cfg_dict["max_completion_length"], num_generations=grpo_cfg_dict["num_generations"], beta=grpo_cfg_dict["beta"], epsilon=grpo_cfg_dict["epsilon_clip"], max_steps=args.max_steps if args.max_steps > 0 else -1, report_to=[])

    cocr_ref = None
    cocr_ref_path = Path(cfg["paths"]["data_dir"]) / "cocr_reference" / f"{short_name}.json"
    if cocr_ref_path.exists():
        with open(cocr_ref_path) as fh:
            cocr_ref = {int(k): v for k, v in json.load(fh).items()}
        logger.info("Loaded CO-CR reference: %d samples", len(cocr_ref))
    else:
        logger.warning("CO-CR reference not found at %s, CO-CR disabled", cocr_ref_path)

    trainer = GRPOTrainer(model=model, reward_funcs=make_reward_fn(cfg, tokenizer, rank, cocr_reference=cocr_ref), args=grpo_args, train_dataset=dataset, processing_class=tokenizer)
    logger.info("Starting CO-GRPO: model=%s epoch=%d", short_name, args.epoch)
    trainer.train()

    if rank == 0:
        ensure_dir(final_save)
        trainer.model.save_pretrained(final_save)
        tokenizer.save_pretrained(final_save)
        logger.info("Saved adapter to %s", final_save)

if __name__ == "__main__":
    main()
