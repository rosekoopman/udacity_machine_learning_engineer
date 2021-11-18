"""Project: Acea Water Analysis
Created: 2021/01/17
Description:
    setup script to install acea package.
Authors:
    Rose Koopman
"""

from setuptools import find_packages
from setuptools import setup

NAME = 'acea'

MAJOR = 0
REVISION = 1
PATCH = 0
DEV = True

VERSION = '{major}.{revision}.{patch}'.format(major=MAJOR, revision=REVISION, patch=PATCH)
FULL_VERSION = VERSION
if DEV:
    FULL_VERSION += '.dev'

TEST_REQUIREMENTS = [
    'pytest>=4.0.2',
    'pytest-pylint>=0.13.0',
]

REQUIREMENTS = []
with open('requirements.txt', 'r') as f:
    for line in f:
        REQUIREMENTS.append(line.strip())

if DEV:
    REQUIREMENTS += TEST_REQUIREMENTS

def setup_package():
    """The main setup method.
    It is responsible for setting up and installing the package.
    :return:
    :rtype: None
    """

    setup(name=NAME,
          version=FULL_VERSION,
          author='Rose Koopman',
          author_email='rfkoopman@gmail.com',
          description="Acea Water Analysis",
          long_description=open("README.md").read(),
          python_requires='>=3.5',
          package_dir={'': 'python'},
          packages=find_packages(where='python'),
          install_requires=REQUIREMENTS,
          tests_require=TEST_REQUIREMENTS,
          classifiers=(
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ),
          )


if __name__ == '__main__':
    setup_package()