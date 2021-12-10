"""Test building the package."""

import subprocess

import pytest
from nanoutils import delete_finally

try:
    import wheel  # noqa: F401
except ModuleNotFoundError as ex:
    WHEEL_EX: "None | ModuleNotFoundError" = ex
else:
    WHEEL_EX = None


@delete_finally('dist', 'build')
@pytest.mark.skipif(WHEEL_EX is not None, reason="Requires wheel")
def test_build() -> None:
    """Test if the package is properly build."""
    subprocess.run('python setup.py sdist bdist_wheel', shell=True, check=True)
