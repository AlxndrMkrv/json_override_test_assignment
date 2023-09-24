from distutils.core import setup


setup(
    name='json_override_test_assignment',
    version='1.0.0',
    packages=['json_override_test_assignment',
              'json_override_test_assignment.tree'],
    data_files=[('/usr/bin/', ['myapp/myapp_run.py']),
                ('/usr/local/etc/myapp', ['myapp/myapp.conf'])],
    url='https://github.com/AlxndrMkrv/json_override_test_assignment',
    license='MIT License',
    author='Alexander Makarov',
    author_email='alexander.makarov@live.com',
    description='Test assignment performing',
    long_description="Long story short"
)
