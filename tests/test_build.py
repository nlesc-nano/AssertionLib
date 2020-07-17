"""Test building the package."""

import sys
import subprocess

import pytest
from nanoutils import delete_finally


@delete_finally('dist', 'build')
@pytest.mark.skipif(sys.version_info[1] <= 6, reason="requires Python 3.7 or higher")
def test_build() -> None:
    """Test if the package is properly build."""
    subprocess.run('python setup.py sdist bdist_wheel', shell=True, check=True)
