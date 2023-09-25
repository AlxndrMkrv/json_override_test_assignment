from PySide2.QtCore import QObject as _QObject, Qt as _Qt, \
    QAbstractItemModel as _QAbstractItemModel, QModelIndex as _QModelIndex, \
    Signal as _Signal
from typing import Any as _Any, Optional as _Optional

from ._item import TreeItem as _TreeItem
from .._configs_handler import Configs as _Configs


class TreeModel (_QAbstractItemModel):
    """The model providing interaction between user interface and JSON
    configuration files. Uses TreeItem as inner data storage"""

    # register signal for value change.
    newOverride = _Signal(dict, name="newOverride")

    def __init__(self, parent: _QObject = None):
        self._root_item = _TreeItem()
        _QAbstractItemModel.__init__(self, parent)

    def clear(self):
        """Override from QAbstractItemModel. Clear the underlying Tree items
        with empty configs"""
        self.load(_Configs())

    def load(self, configs: _Configs):
        """Override from QAbstractItemModel. Fills the underlying Tree items
        with given configs"""
        assert isinstance(configs, _Configs)

        self.beginResetModel()
        self._root_item = _TreeItem.load(configs)
        self._root_item.value_type = type(configs)
        self.endResetModel()

        return True

    def data(self, index: _QModelIndex, role: _Qt.ItemDataRole) -> _Any:
        """
        Override from QAbstractItemModel. Returns underlying Tree item fields
        """
        if not index.isValid():
            return None

        item = index.internalPointer()  # type: _TreeItem

        if role == _Qt.DisplayRole:
            column_name = _TreeItem.Fields[index.column()]
            return item.get_field(column_name)

        elif role == _Qt.EditRole and \
                index.column() == _TreeItem.Fields.index("value"):
            return item.value

    def __create_override(self, index: _QModelIndex,
                          override: _Optional[dict]) -> dict:
        """Recursively extract override dict from index of changed value"""
        item = index.internalPointer()  # type: _TreeItem

        # Stop when None reached
        if item is None:
            return override

        # Initialize override value
        elif override is None:
            # if item at index is list, go one level up and gather all values
            if item.value_type == list:
                parent = index.parent().internalPointer()  # type: _TreeItem
                value = [parent.child(i).value
                         for i in range(parent.child_count())]
                return self.__create_override(index.parent().parent(),
                                              {parent.key: value})
            #
            else:
                return self.__create_override(index.parent(),
                                              {item.key: item.value})

        # Continue to folding dictionaries
        else:
            return self.__create_override(index.parent(), {item.key: override})

    def setData(self, index: _QModelIndex, value: _Any, role: _Qt.ItemDataRole):
        """
        Override from QAbstractItemModel. Catch value change and emit
        'newOverride' signal
        """

        if role == _Qt.EditRole:
            item = index.internalPointer()  # type: _TreeItem
            if index.column() == _TreeItem.Fields.index("value") and \
                    item.is_leaf():
                # set item value
                item.value = str(value)

                # extract override from index and emit the signal
                override = self.__create_override(index, None)
                self.newOverride.emit(override)
                return True

        return False

    def headerData(self, section: int, orientation: _Qt.Orientation,
                   role: _Qt.ItemDataRole):
        """Override from QAbstractItemModel

        For the JsonModel, it returns only data for columns (orientation = Horizontal)

        """
        if role != _Qt.DisplayRole:
            return None

        if orientation == _Qt.Horizontal:
            return _TreeItem.Fields[section]

    def index(self, row: int, column: int,
              parent=_QModelIndex()) -> _QModelIndex:
        """Override from QAbstractItemModel

        Return index according row, column and parent

        """
        if not self.hasIndex(row, column, parent):
            return _QModelIndex()

        if not parent.isValid():
            parentItem = self._root_item
        else:
            parentItem = parent.internalPointer()

        child_item = parentItem.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return _QModelIndex()

    def parent(self, index: _QModelIndex) -> _QModelIndex:
        if not index.isValid():
            return _QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self._root_item:
            return _QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=_QModelIndex()):
        """
        Override from QAbstractItemModel. Return row count from parent index
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent=_QModelIndex()):
        """
        Override from QAbstractItemModel. Return number of columns
        """
        return len(_TreeItem.Fields)

    def flags(self, index: _QModelIndex) -> _Qt.ItemFlags:
        flags = _QAbstractItemModel.flags(self, index)

        if index.column() == _TreeItem.Fields.index("value"):
            return _Qt.ItemIsEditable | flags
        else:
            return flags
