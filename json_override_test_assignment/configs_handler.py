import json as _json
from tempfile import gettempdir as _gettempdir
import os as _os
from functools import reduce as _reduce
from typing import List as _List, Dict as _Dict, Iterable as _Iterable


ValueType = str | _List[str] | _Dict[str, str]


class Configs (dict):
    def __init__(self, config_dir: str = _gettempdir()):
        if not _os.path.isdir(config_dir):
            raise NotADirectoryError(f"{config_dir} not found")
        elif not _os.access(config_dir, _os.R_OK):
            raise PermissionError(f"{config_dir} can't be read")

        def content(filename: str):
            with open(filename) as f:
                return _json.load(f)

        dict.__init__(self, {_os.path.splitext(_os.path.basename(f))[0]:
                                 content(f)
                             for f in _os.listdir(config_dir)
                             if f.startswith("config") and f.endswith(".json")})

    def get_value(self, config: str, param: str) -> ValueType | None:
        value = _reduce(lambda d, a: d.get(a, {}), [config, param], self)
        return value if value != {} else None


class Override (Configs):
    def __init__(self, filename: str = f"{_gettempdir()}/override.json"):
        self.__filename = filename
        content = {}

        # Read file if already exists
        if _os.path.isfile(filename):
            # check RW permissions
            if not _os.access(filename, _os.W_OK | _os.R_OK):
                raise PermissionError(f"{filename} inaccessible")

            # load data from file
            with open(filename) as f:
                content = _json.load(f)

        # Write empty file if not present
        else:
            # check if directory writable
            if not _os.access(_os.path.dirname(filename), _os.W_OK):
                raise PermissionError(f"{_os.path.dirname(filename)} "
                                      f"inaccessible")

            with open(filename, 'w') as f:
                _json.dump({}, f)

        # initialize grandparent
        dict.__init__(self, content)

    def set_value(self, config: str, param: str, value: ValueType):
        """

        :param config:
        :param param:
        :param value:
        :return:
        """
        if isinstance(value, dict):
            if param in self[config]:
                self[config][param].update(value)
            else:
                self[config].update({param: value})
        else:
            self[config].update({param: value})
        self.dump()

    def dump(self):
        """ Dump content into override file """
        with open(self.__filename, 'w') as f:
            _json.dump(self, f)


class Handler:
    def __init__(self, config_dir: str, override_file: str):
        self.__configs = Configs(config_dir)
        self.__override = Override(override_file)

    def get_configs(self) -> _Iterable[str]:
        return self.__configs.keys()

    def get_params(self, config: str) -> _Iterable[str] | None:
        return self.__configs[config].keys() \
            if config in self.__configs else None

    def get_value(self, config: str, param: str) -> ValueType | None:
        value = self.__configs.get_value(config, param)
        override = self.__override.get_value(config, param)

        if isinstance(value, ValueType) and override is None:
            return value
        elif isinstance(value, dict) and isinstance(override, dict):
            return value | override # some fancy magic
        elif isinstance(override, ValueType):
            return override
        else:
            raise ValueError(f"Unexpected value \"{value}\" and "
                             f"override \"{override}\"")

    def set_value(self, config: str, param: str, value: ValueType):
        self.__override.set_value(config, param, value)
