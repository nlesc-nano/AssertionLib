"""Test the :mod:`sphinx` documentation generation."""

import sys
from os.path import join

import pytest
from nanoutils import delete_finally

try:
    from sphinx.application import Sphinx
except ModuleNotFoundError as ex:
    SPHINX_EX: "None | ModuleNotFoundError" = ex
else:
    SPHINX_EX = None

SRCDIR = CONFDIR = 'docs'
OUTDIR = join('tests', 'test_files', 'build')
DOCTREEDIR = join('tests', 'test_files', 'build', 'doctrees')


@delete_finally(OUTDIR)
@pytest.mark.skipif(SPHINX_EX is not None, reason="Requires sphinx")
@pytest.mark.skipif(sys.version_info[1] <= 6, reason="requires Python 3.7 or higher")
def test_sphinx_build() -> None:
    """Test :meth:`sphinx.application.Sphinx.build`."""
    app = Sphinx(SRCDIR, CONFDIR, OUTDIR, DOCTREEDIR,
                 buildername='html', warningiserror=True)
    app.build(force_all=True)
