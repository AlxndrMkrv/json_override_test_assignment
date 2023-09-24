# JSON override test assignment

The goal of the assignment is to create Qt application with following functionality:

- display content of _config*.json_ files contained a certain directory;
- override config fields with values recorded in _overrides.json_;
- save changes made using the GUI to _overrides.json_;

Also the application must be distributed as a .deb package with a certan rules.


## Project structure

``` bash
├── run.py  # simple script to import application modules and run them
├── json_override_test_assignment
|   ├── __init__.py  # Declares public interface of the package
|   ├── _app.py  # QApplication derivative holding top-level logic
|   ├── _paths.py  # Contains pathes to JSON files
|   ├── _configs_handler.py  # Core logic providing operations with configs
|   ├── _misc.py  # Contains helper function generating config*.json files
|   └── tree
|       ├── __init__.py  # Custom QModelView package interface
|       ├── _item.py  # Tree item mapping JSON fields to tree columns
|       └── _model.py  # Model view representing JSON documents
├── test
|   └── test_override.py  # Test file to check core logic
├── README.md  # this file
└── .gitignore
```
