import unittest
from copy import deepcopy
from json_override_test_assignment import Configs
from tempfile import mkdtemp
import shutil


class TestOverrideMethods(unittest.TestCase):
    def test_io(self):
        original = {'a': {'b': {'c': [1, 2, 3],
                                'd': 4},
                          'e': 5,
                          'f': [6,7]},
                    'g': 8}
        tmp_dir = mkdtemp()
        Configs(original).dump(f"{tmp_dir}/test.json")
        restored = Configs.from_override_file(f"{tmp_dir}/test.json")
        shutil.rmtree(tmp_dir)
        self.assertEqual(original, restored)

    def test_override(self):
        alter = Configs.override({'a': {'b': {'c': 1, 'd': 2},
                                        'e': 3}},
                                 {'a': {'b': {'c': 9}}})
        self.assertEqual(alter, {'a': {'b': {'c': 9, 'd': 2},
                                       'e': 3}})

    def test_diff(self):
        original = {'a': {'b': 1,
                          'c': [2, 3, 4],
                          'd': {'e': 5,
                                'f': [6, 7]}
                          }
                    }
        altered = deepcopy(original)
        altered['a']['d']['e'] = 90

        diff = Configs.diff(original, altered)
        self.assertEqual(diff, {'a': {'d': {'e': 90}}})

        altered['a']['b'] = 91
        diff = Configs.diff(original, altered)
        self.assertEqual(diff, {'a': {'b': 91,
                                      'd': {'e': 90}}})

        altered['a']['c'] = [2, 92, 4]
        diff = Configs.diff(original, altered)
        self.assertEqual(diff, {'a': {'b': 91,
                                      'c': [2, 92, 4],
                                      'd': {'e': 90}}})



