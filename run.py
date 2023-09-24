#!/bin/env python3

import os
import sys
from argparse import ArgumentParser
from json_override_test_assignment import Application, \
    CONFIGS_DIRECTORY, OVERRIDE_FILE


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def is_valid_dir(parser, arg):
    if not os.path.isdir(arg):
        parser.error(f"The directory {arg} doesn't exist!")
    elif not len([f for f in os.listdir(arg)
                  if f.startswith("config") and f.endswith(".json")]):
        parser.error(f"The directory {arg} doesn't contain any config*.json")
    else:
        return arg


if __name__ == "__main__":
    arg_parser = ArgumentParser("JSON override test assignment application")
    arg_parser.add_argument("--configs", type=str, default=CONFIGS_DIRECTORY,
                            help="path to directory with config*.json")
    arg_parser.add_argument("--overrides", type=str, default=OVERRIDE_FILE,
                            help="path to overrides.json file")
    args = arg_parser.parse_args()

    app = Application("json_override_test_assignment",
                      args.configs, args.overrides)
    sys.exit(app.exec())
