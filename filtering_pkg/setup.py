"""
Usage: pip install .[dev]
"""

import re
import sys

from setuptools import setup

# name of the package
PKGNAME = 'filtering_AF'
# in case there is a collective super package, i.e. a mother namespace
# if not PKGNAME_QUALIFIED = PKGNAME
#PKGNAME_QUALIFIED = 'tools.' + PKGNAME

PKGNAME_QUALIFIED = PKGNAME
# minimal python version, will not install if someone tries to install with
# lower version
MIN_PYTHON_VERSION = (2, )

# what is needed for a user:  pip install -e .
install_require = ['numpy','scipy']
# what is needed for a tester:  pip install -e .[test]
test_require = ['pytest', 'dill', 'tox']
# what is needed for a developer: pip install -e .[dev]
dev_require = test_require + [
    'pytest-cov', 'yapf==0.20', 'prospector', 'pre-commit', 'sphinx',
    'sphinx-rtd-theme', 'ipython'
]


# throw error if version is too low
if sys.version_info < MIN_PYTHON_VERSION:
    raise ValueError(
        'only Python {} and higher are supported'.format(
            '.'.join(map(str, MIN_PYTHON_VERSION))
        )
    )

setup(
    name=PKGNAME_QUALIFIED,
    version="1.0",
    packages=[PKGNAME_QUALIFIED],
    # url='http://frescolinogroup.github.io/frescolino/pyhdf5io/' +
    # '.'.join(VERSION.split('.')[:2]),
    include_package_data=True,
    author='Michael Kugler',
    author_email='',
    # description=DESCRIPTION,
    install_requires=install_require,
    extras_require={
        'test': test_require,
        'dev': dev_require
    },
    # long_description=README,
    classifiers=[  # yapf: disable
        # 'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities'
    ],
    # license='Apache',
)
