"""Tests for the :class:`AssertionManager<assertionlib.manager.AssertionManager>` class."""

from os.path import dirname, join

from assertionlib import assertion

PATH: str = dirname(__file__)
TEST_DIR: str = join(PATH, 'test_files', 'test_dir')
TEST_FILE: str = join(PATH, 'test_files', 'test_file.txt')
TEST_DUMMY: str = join(PATH, 'test_files', 'does_not_exist')


def test_isabs() -> None:
    """Test :meth:`AssertionManager.isabs`."""
    assertion.isabs(TEST_FILE)
    assertion.isabs(TEST_DIR)
    assertion.isabs(TEST_DUMMY)
    assertion.isabs('bob', invert=True)
    assertion.isabs(5, 6, 7, 8, exception=TypeError)
    assertion.isabs([5], exception=TypeError)


def test_isdir() -> None:
    """Test :meth:`AssertionManager.isdir`."""
    assertion.isdir(TEST_FILE, invert=True)
    assertion.isdir(TEST_DIR)
    assertion.isdir(TEST_DUMMY, invert=True)
    assertion.isdir('bob', invert=True)
    assertion.isdir(5, 6, 7, 8, exception=TypeError)
    assertion.isdir([5], exception=TypeError)


def test_isfile() -> None:
    """Test :meth:`AssertionManager.isfile`."""
    assertion.isfile(TEST_FILE)
    assertion.isfile(TEST_DIR, invert=True)
    assertion.isfile(TEST_DUMMY, invert=True)
    assertion.isfile('bob', invert=True)
    assertion.isfile(5, 6, 7, 8, exception=TypeError)
    assertion.isfile([5], exception=TypeError)


def test_islink() -> None:
    """Test :meth:`AssertionManager.islink`."""
    assertion.islink(TEST_FILE, invert=True)
    assertion.islink(TEST_DIR, invert=True)
    assertion.islink(TEST_DUMMY, invert=True)
    assertion.islink('bob', invert=True)
    assertion.islink(5, 6, 7, 8, exception=TypeError)
    assertion.islink([5], exception=TypeError)


def test_ismount() -> None:
    """Test :meth:`AssertionManager.ismount`."""
    assertion.ismount(TEST_FILE, invert=True)
    assertion.ismount(TEST_DIR, invert=True)
    assertion.ismount(TEST_DUMMY, invert=True)
    assertion.ismount('bob', invert=True)
    assertion.ismount(5, 6, 7, 8, exception=TypeError)
    assertion.ismount([5], exception=TypeError)
