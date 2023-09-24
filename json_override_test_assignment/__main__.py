"""Package run script"""

import sys
from . import Application

if __name__ == "__main__":
    app = Application("json_override_test_assignment")
    sys.exit(app.exec())
