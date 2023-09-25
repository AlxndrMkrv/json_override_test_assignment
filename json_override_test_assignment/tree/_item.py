try:
    from typing import Self as _Self
except ImportError:
    _Self = "TreeItem"
from typing import Union as _Union
from .._configs_handler import Configs as _Configs


class TreeItem:
    """Underlying values storage for TreeModel"""
    # note: Fields a used both in this class and as column names for TreeModel
    Fields: tuple = ("key", "value")

    def __init__(self, parent: _Self = None):
        self.__parent = parent
        self.__fields = dict.fromkeys(TreeItem.Fields, "") | {"type": None,
                                                              "is_leaf": False}
        self.__children = []

    def append_child(self, item: _Self):
        """Attach given item to tree"""
        self.__children.append(item)

    def child(self, row: int) -> _Self:
        """Return the children at given row"""
        return self.__children[row]

    def parent(self) -> _Self:
        """Return the parent of the current item"""
        return self.__parent

    def child_count(self) -> int:
        """Return the number of children of the current item"""
        return len(self.__children)

    def row(self) -> int:
        """Return the row where the current item occupies in the parent"""
        return self.__parent.__children.index(self) if self.__parent else 0

    def get_field(self, name: str) -> str:
        """Return field value with given name"""
        return self.__fields.get(name, "")

    @property
    def key(self) -> str:
        return self.__fields.get("key", "")

    @key.setter
    def key(self, key: str):
        self.__fields.update({"key": key})

    @property
    def value(self) -> str:
        return self.__fields.get("value", "")

    @value.setter
    def value(self, value: str):
        self.__fields.update({"value": value})

    @property
    def value_type(self):
        return self.__fields.get("type", None)

    @value_type.setter
    def value_type(self, value_type):
        self.__fields.update({"type": value_type})

    def is_leaf(self):
        return self.__fields.get("is_leaf", None)

    @classmethod
    def load(cls, value: _Union[_Configs, dict, list, str],
             parent: _Self = None, sort=True) -> _Self:
        """Recursively build items tree from given JSON configuration data"""
        root_item = TreeItem(parent)
        root_item.key = "root"

        if isinstance(value, (_Configs, dict)):
            items = sorted(value.items() if sort else value.items())
            is_config_item = isinstance(value, _Configs)
            for key, value in items:
                child = cls.load(value, root_item)
                child.__fields.update({"key": key,
                                       "type": _Configs if is_config_item
                                       else dict})
                root_item.append_child(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load(value, root_item)
                child.__fields.update({"key": index,
                                       "type": list})
                root_item.append_child(child)

        else:
            root_item.__fields.update({"value": value,
                                       "type": type(value),
                                       "is_leaf": True})

        return root_item


