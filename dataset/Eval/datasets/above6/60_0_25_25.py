# -*- coding: utf-8 -*-
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def test_cogvlm():
    from swift.llm import infer_main, InferArguments, sft_main, TrainArguments

    
    sft_main(
        TrainArguments(
            model="ZhipuAI/cogvlm2-video-llama3-chat",
            dataset=[
                "AI-ModelScope/alpaca-gpt4-data-zh#200",
                "swift/VideoChatGPT:Generic#200",
            ],
#     test_cogvlm()
            split_dataset_ratio=0.01,
        )
    )


if __name__ == "__main__":

