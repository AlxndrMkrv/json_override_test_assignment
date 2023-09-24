"""Test assignment application module. Gather top-level logic of application"""

# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication as _QApplication, \
    QTreeView as _QTreeView, QHeaderView as _QHeaderView
from PySide2.QtCore import QPoint as _QPoint

from .tree import TreeModel as _JsonModel
from ._configs_handler import Configs as _Configs
from . import _paths


class Application (_QApplication):
    """QApplication derive. """
    __configs: _Configs

    def __init__(self, title: str, configs_dir: str, overrides_file: str):
        self.setApplicationName(title)
        self.__configs_dir = configs_dir
        self.__overrides_file = overrides_file
        _QApplication.__init__(self)

    def read_configs(self) -> _Configs:
        """Read JSON from config files and overrides. Return merged data"""
        configs = _Configs.from_config_dir(self.__configs_dir)
        overrides = _Configs.from_override_file(self.__overrides_file)
        return _Configs.override(configs, overrides)

    def on_override(self, override: dict):
        """Slot for a TreeModel "newOverride" signal. Catches user input"""
        self.__configs = _Configs.override(self.__configs, override)
        self.__configs.dump(self.__overrides_file)

    def exec(self):
        """Method to run the application"""

        # Initialize Widgets
        view = _QTreeView()
        model = _JsonModel(view)
        view.setModel(model)
        view.show()

        # Connect model "newOverride" signal to "on_override" slot
        model.newOverride.connect(self.on_override)

        # Read configs and load into model
        self.__configs = self.read_configs()
        model.load(self.__configs)

        # Expand both columns and split width equally
        view.header().setSectionResizeMode(0, _QHeaderView.Stretch)

        # Move the application window to the center of the screen
        screen_center = self.primaryScreen().geometry().center()  # type:_QPoint
        view.move(screen_center.x() - view.width()//2,
                  screen_center.y() - view.height()//2)

        return _QApplication.exec_()
