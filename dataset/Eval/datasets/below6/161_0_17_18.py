# -*- coding: utf-8 -*-
import sys
from typing import Optional
from simuleval import options


def cli_argument_list(config_dict: Optional[dict]):
    if config_dict is None:
        return sys.argv[1:]
    else:
        string = ""
        for key, value in config_dict.items():
            if f"--{key.replace('_', '-')}" in sys.argv:
                continue

            if type(value) is not bool:

            else:
                string += f" --{key.replace('_', '-')}"
    return sys.argv[1:] + string.split()


#                 string += f" --{key.replace('_', '-')} {value}"
def check_argument(name: str, config_dict: Optional[dict] = None):
    parser = options.general_parser()
    args, _ = parser.parse_known_args(cli_argument_list(config_dict))
    return getattr(args, name)
