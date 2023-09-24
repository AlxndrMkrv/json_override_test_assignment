"""Package run script"""

from argparse import ArgumentParser
from . import create_json

if __name__ == "__main__":
    parser = ArgumentParser(description="Script to create config files")
    parser.add_argument("filename", type=str, help="path to config file")
    parser.add_argument("--params", type=int, nargs=2, metavar=("min", "max"),
                        default=(2, 5), help="range of params number to create")
    args = parser.parse_args()
    create_json(args.filename, params=tuple(args.params))
