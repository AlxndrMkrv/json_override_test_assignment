from json import dump as _dump
from random import randint as _randint, choice as _choice
import os as _os
from argparse import ArgumentParser as _ArgumentParser


def create_json(filename: str, params: tuple = (2, 5)):
    """
    Create .json file with appropriate format
    :param filename: full path to a target .json file
    :param params: (min, max) range for the number of params in file
    :return:
    """

    # assert 'filename' is valid path to *.json file
    assert _os.path.isdir(_os.path.dirname(filename)), \
        f"{create_json.__name__}: 'filename' must contain existing directory"
    assert _os.path.splitext(filename)[1] == ".json", \
        f"{create_json.__name__}: 'filename' extension must be \".json\""

    # assert 'params' is valid (min, max) tuple
    assert isinstance(params, tuple) and len(params) == 2 and \
           all(isinstance(i, int) and i > 0 for i in params) and \
           params[1] > params[0], f"{create_json.__name__}: " \
                                  f"'params' must contain (min, max) tuple"

    # create future json dictionary...
    content = dict.fromkeys([f"param{i+1}"
                             for i in range(_randint(params[0], params[1]))],
                            None)
    # ... and fill it
    for k in content:
        param_type = _choice((str, list, dict))
        if param_type == str:
            content[k] = "value"
        elif param_type == list:
            content[k] = [f"value{i+1}" for i in range(_randint(params[0],
                                                                params[1]))]
        else:
            content[k] = {f"key{i+1}": f"value{i+1}"
                          for i in range(_randint(params[0], params[1]))}

    # save json to file
    with open(filename, 'w') as f:
        _dump(content, f, indent=2)
        f.write('\n')

