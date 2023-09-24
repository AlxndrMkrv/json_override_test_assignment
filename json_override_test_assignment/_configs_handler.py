"""Module that takes care of "config*.json" and "overrides.json" files"""

import json as _json
import os as _os
from typing import List as _List, Dict as _Dict
from copy import deepcopy as _deepcopy


ValueType = str | _List[str] | _Dict[str, str]


class Configs (dict):
    """
    Holds JSON data from either "config*.json" or "overrides.json" in same
    format
    """

    @staticmethod
    def from_config_dir(config_dir: str):
        """
        Read "config*.json" files from given dir and join JSONs into single dict
        """

        # Check if directory exists
        if not _os.path.isdir(config_dir):
            raise NotADirectoryError(f"Configs directory \"{config_dir}\" "
                                     f"not found")

        # check permission to read
        if not _os.access(config_dir, _os.R_OK):
            raise PermissionError(f"Configs directory \"{config_dir}\" is "
                                  f"read-protected")

        # Nested function to load JSON data from config file
        def content(filename: str):
            # pylint: disable=invalid-name
            with open(filename, encoding="ascii") as f:
                return _json.load(f)

        # Get "config*.json" files from given directory and populate dictionary
        # with JSON data from them
        return Configs({_os.path.splitext(_os.path.basename(f))[0]:
                            content(f"{config_dir}/{f}")
                        for f in _os.listdir(config_dir)
                        if f.startswith("config") and f.endswith(".json")})

    @staticmethod
    def from_override_file(filename: str):
        """Read JSON from overrides.json"""
        # Check file exists
        if not _os.path.isfile(filename):
            raise FileNotFoundError(f"Override file \"{filename}\" not found")

        # Check permissions to read-write
        if not _os.access(filename, _os.W_OK | _os.R_OK):
            raise PermissionError(f"Override file \"{filename}\" is "
                                  f"RW-protected")

        # Initialize file if empty
        if not _os.path.getsize(filename):
            # pylint: disable=invalid-name
            with open(filename, 'w', encoding="ascii") as f:
                _json.dump({}, f)

        # Load data from file
        # pylint: disable=invalid-name
        with open(filename, encoding="ascii") as f:
            return Configs(_json.load(f))

    @staticmethod
    def override(orig: dict, over: dict) -> "Configs":
        """Override values of given dict with given changeset"""
        assert isinstance(orig, dict)
        assert isinstance(over, dict)

        alter_dict = _deepcopy(orig)
        for key in orig.keys() & over.keys():
            if isinstance(orig[key], dict):
                alter_dict[key].update(
                    Configs.override(alter_dict[key], over[key]))
            else:
                alter_dict[key] = over[key]

        return Configs(alter_dict)

    @staticmethod
    def diff(orig: dict, alter: dict) -> "Configs":
        """Show difference between original dict and altered. In other words
        produces "overrides.json" content"""
        assert isinstance(orig, dict)
        assert isinstance(alter, dict)

        diff_dict = {}
        for key in filter(lambda k: orig[k] != alter[k], alter):
            if isinstance(orig[key], dict):
                diff_dict[key] = Configs.diff(orig[key], alter[key])
            else:
                diff_dict[key] = alter[key]

        return Configs(diff_dict)

    def dump(self, filename: str):
        """Dump JSON data into given file"""
        # pylint: disable=invalid-name
        with open(filename, 'w', encoding="ascii") as f:
            _json.dump(self, f)
            f.write('\n')
