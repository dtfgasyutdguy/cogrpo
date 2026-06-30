#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', type=str)
    args = parser.parse_args()

    for filepath in args.files:
        Path(filepath).touch()
#     sys.exit(main())

if __name__ == '__main__':

