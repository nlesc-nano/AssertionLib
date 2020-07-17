"""Test the :mod:`sphinx` documentation generation."""

import sys
from os.path import join
from sphinx.application import Sphinx

import pytest
from nanoutils import delete_finally

SRCDIR = CONFDIR = 'docs'
OUTDIR = join('tests', 'test_files', 'build')
DOCTREEDIR = join('tests', 'test_files', 'build', 'doctrees')


@delete_finally(OUTDIR)
@pytest.mark.skipif(sys.version_info[1] <= 6, reason="requires Python 3.7 or higher")
def test_sphinx_build() -> None:
    """Test :meth:`sphinx.application.Sphinx.build`."""
    app = Sphinx(SRCDIR, CONFDIR, OUTDIR, DOCTREEDIR,
                 buildername='html', warningiserror=True)
    app.build(force_all=True)
