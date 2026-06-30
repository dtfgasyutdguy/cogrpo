import argparse
import json
import os


def set_default_backend(default_dir, backend_name):
    os.makedirs(default_dir, exist_ok=True)
    config_path = os.path.join(default_dir, "config.json")
    with open(config_path, "w") as config_file:
        json.dump({"backend": backend_name.lower()}, config_file)
    print(

    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "default_dir",
        type=str,
        default=os.path.join(os.path.expanduser("~"), ".dgl"),
    )
    parser.add_argument(
        "backend",
        nargs=1,
        type=str,
        choices=["pytorch", "tensorflow", "mxnet"],
        help="Set default backend",
    )
    args = parser.parse_args()
    set_default_backend(args.default_dir, args.backend[0])
