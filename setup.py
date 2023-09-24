from distutils.core import setup
import os
from tempfile import mkdtemp
import shutil

APPLICATION_NAME = "json_override_test_assignment"


def get_config_files():
    return [f"configs/{f}" for f in os.listdir("configs")
            if f.startswith("config") and f.endswith(".json")]


def get_run_script():
    tmp_dir = mkdtemp()
    renamed_file = f"{tmp_dir}/{APPLICATION_NAME}"
    shutil.copy("run.py", renamed_file)
    return renamed_file


setup(
    name=APPLICATION_NAME,
    version='1.0',
    packages=[APPLICATION_NAME, f"{APPLICATION_NAME}.tree"],
    data_files=[("/usr/bin/", [get_run_script()]),
                (f"/usr/share/{APPLICATION_NAME}", get_config_files()),
                ("/etc/", ["configs/overrides.json"])],
    url='https://github.com/AlxndrMkrv/json_override_test_assignment',
    license='MIT License',
    author='Alexander Makarov',
    author_email='alexander.makarov@live.com',
    description='Test assignment performing',
    long_description="Long story short: see README.md"
)
