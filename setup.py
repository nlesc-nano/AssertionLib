#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Dict

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit assertionlib/__version__.py
version: Dict[str, str] = {}
version_path = os.path.join(here, 'assertionlib', '__version__.py')
with open(version_path, encoding='utf-8') as f:
    exec(f.read(), version)

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

# Requirements for building the documentation
docs_require = [
    'sphinx>=2.4,<3.1',
    'sphinx_rtd_theme'
]

# Requirements for building wheels
build_require = [
    'twine',
    'wheel',
]

tests_require_no_optional = [
    'pytest>=5.4.0',
    'pytest-cov',
    'pytest-mypy>=0.6.2',
]

# Requirements for running tests
tests_require = [
    'numpy',
    'pandas',
]
tests_require += tests_require_no_optional
tests_require += docs_require
tests_require += build_require

setup(
    name='AssertionLib',
    version=version['__version__'],
    description='A package for performing assertions and providing informative exception messages.',
    long_description=f'{readme}\n\n',
    long_description_content_type='text/x-rst',
    author=['B. F. van Beek'],
    author_email='b.f.van.beek@vu.nl',
    url='https://github.com/nlesc-nano/AssertionLib',
    packages=['assertionlib'],
    package_dir={'assertionlib': 'assertionlib'},
    package_data={'assertionlib': ['*.rst', '*.pyi', 'py.typed']},
    include_package_data=True,
    license='Apache Software License',
    zip_safe=False,
    keywords=[
        'assertion',
        'assertions',
        'assertion-library',
        'testing',
        'unit-testing',
        'python-3',
        'python-3-6',
        'python-3-7',
        'python-3-8',
        'python-3-9',
        'python-3-10',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Nano-Utils>=0.4.1; python_version<"3.9"',
        'Nano-Utils>=1.1.2; python_version>="3.9"',
    ],
    setup_requires=['pytest-runner'] + docs_require,
    tests_require=tests_require,
    extras_require={
        'doc': docs_require,
        'test': tests_require,
        'test_no_optional': tests_require_no_optional,
        'build': build_require,
    }
)
