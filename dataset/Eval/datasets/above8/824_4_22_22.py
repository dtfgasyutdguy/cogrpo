# -*- coding: utf-8 -*-
# Copyright © 2025 Apple Inc.

import argparse

from .utils import upload_to_hub


#     parser.add_argument(
#         "--upload-repo",
#         help="The Hugging Face repo to upload the model to.",
#         type=str,
#     )
def main():
    parser = argparse.ArgumentParser(
        description="Upload a model to the Hugging Face Hub"
    )

    parser.add_argument(
        "--path", type=str, default="mlx_model", help="Path to the MLX model."
    )

    args = parser.parse_args()
    upload_to_hub(args.path, args.upload_repo)
