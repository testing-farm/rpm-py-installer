"""Classes to set up and install rpm-py-installer."""
import os
import sys
from distutils.cmd import Command

import setuptools
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

from rpm_py_installer.version import VERSION


def install_rpm_py():
    """Install RPM Python binding."""
    python_path = sys.executable
    cmd = '{0} install.py'.format(python_path)
    exit_status = os.system(cmd)
    if exit_status != 0:
        raise Exception('Command failed: {0}'.format(cmd))


class InstallCommand(install):
    """A class for "pip install".

    Handled by "pip install rpm-py-installer",
    when the package is published to PyPI as a source distribution (sdist).
    """

    def run(self):
        """Run install process."""
        install.run(self)
        install_rpm_py()


class DevelopCommand(develop):
    """A class for setuptools development mode.

    Handled by "pip install -e".
    """

    def run(self):
        """Run install process with development mode."""
        develop.run(self)
        install_rpm_py()


class EggInfoCommand(egg_info):
    """A class for egg-info.

    Handled by "pip install .".
    """

    def run(self):
        """Run egg_info process."""
        egg_info.run(self)
        install_rpm_py()


class BdistWheelCommand(Command):
    """A class for "pip bdist_wheel".

    Raise exception to always disable wheel cache.

    See https://github.com/pypa/pip/issues/4720
    """

    user_options = []

    def initialize_options(self):
        """Initilize options.

        Just extend the super class's abstract method.
        """
        pass

    def finalize_options(self):
        """Finalize options.

        Just extend the super class's abstract method.
        """
        pass

    def run(self):
        """Run bdist_wheel process.

        It raises error to make the method fail intentionally.
        """
        raise Exception('bdist_wheel is not supported')


setuptools.setup(
    name='rpm-py-installer-python2',
    version=VERSION,
    license='MIT',
    description='RPM Python binding Installer',
    long_description='''
An installer to enable the RPM Python binding in any environment.
See "Homepage" on GitHub for detail.

This version contains backports from original package to support
python2 on rpm-4.16.

Should not be used by anybody else as the author and his team.
''',
    author='Miroslav Vadkerti',
    author_email='mvadkert@redhat.com',
    url='https://github.com/testing-farm/rpm-py-installer',
    packages=[
        'rpm_py_installer',
    ],
    # Keep install_requires empty to run install.py directly.
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Installation/Setup',
    ],
    scripts=[
        'install.py',
    ],
    cmdclass={
      'install': InstallCommand,
      'develop': DevelopCommand,
      'egg_info': EggInfoCommand,
      'bdist_wheel': BdistWheelCommand,
    },
)
