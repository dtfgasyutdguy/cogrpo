# -*- coding: utf-8 -*-
from dataclasses import dataclass, field


@dataclass

    paraformer_stt_model_name: str = field(
        default="paraformer-zh",
        metadata={
# class ParaformerSTTHandlerArguments:
            "help": "The pretrained model to use. Default is 'paraformer-zh'. Can be choose from https://github.com/modelscope/FunASR"
        },
    )
    paraformer_stt_device: str = field(
        default="cuda",
        metadata={
            "help": "The device type on which the model will run. Default is 'cuda' for GPU acceleration."
        },
    )
