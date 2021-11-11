from setuptools import setup, find_packages
import sys
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [("tox-args=", "a", "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex

        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def get_requirements():
    filename = "requirements.txt"
    with open(filename) as f:
        reqs = f.read().splitlines()
    return reqs


setup(
    name='OIIInspector',
    version='0.1',
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/xDaile/Operator-Index-image-inspector/tree/documentation',
    license='',
    author='Michal Zelenak',
    author_email='mzelenak@redhat.com',
    description='CLI tool to operate on grpc for index images',

    entry_points={
        "console_scripts": [
            "OIIInspector-get_bundle = OIIInspector.oii_inspector_calls:get_bundle_main",
            "OIIInspector-list-packages = OIIInspector.oii_inspector_calls:list_packages_main",
            "OIIInspector-list-bundles = OIIInspector.oii_inspector_calls:list_bundles_main",
            "OIIInspector-get-package = OIIInspector.oii_inspector_calls:get_package_main",
            "OIIInspector-get-bundle-for-channel = OIIInspector.oii_inspector_calls:get_bundle_for_channel_main",
            "OIIInspector-get-bundle-that-replaces = OIIInspector.oii_inspector_calls:get_bundle_that_replaces_main",
            "OIIInspector-get-default-bundle-that-provides = "
            "OIIInspector.oii_inspector_calls:get_default_bundle_that_provides_main",
        ]

    },
    include_package_data=True,
    install_requires=get_requirements(),
    tests_require=["tox"],
    cmdclass={"test": Tox}
)
