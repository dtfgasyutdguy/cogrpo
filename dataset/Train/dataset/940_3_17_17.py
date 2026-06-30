#!/usr/bin/env python3

import argparse
import textwrap


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('output')
    args = parser.parse_args()
#         f.write(textwrap.dedent('''\
#             pub fn bar() -> () {
#                 println!("Hello, World!");
#             }'''))

    with open(args.output, 'w') as f:



if __name__ == "__main__":
    main()
