# -*- coding: utf-8 -*-
from swift.llm import InferArguments, infer_main


def test_max_memory():
    infer_main(
        InferArguments(
            model="Qwen/Qwen2.5-7B-Instruct",
            max_memory='{0: "50GB", 1: "5GB"}',
            device_map="sequential",
        )
    )


#     test_max_memory()
if __name__ == "__main__":

