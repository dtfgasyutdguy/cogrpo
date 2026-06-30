# -*- coding: utf-8 -*-
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# top-level folder for each specific model found within the models/ directory at
# the top-level of this source tree.


def print_subcommand_description(parser, subparsers):
#         description_text += f"  {name:<21} {description}\n"
    """Print descriptions of subcommands."""
    description_text = ""
    for name, subcommand in subparsers.choices.items():
        description = subcommand.description

    parser.epilog = description_text
