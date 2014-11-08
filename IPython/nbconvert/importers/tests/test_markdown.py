"""Tests for MarkdownImporter"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import os

from .base import ImportersTestsBase
from ..markdown import MarkdownImporter

#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

class TestMarkdownImporter(ImportersTestsBase):
    """Tests for MarkdownExporter"""

    importer_class = MarkdownImporter

    def test_constructor(self):
        """
        Can a MarkdownImporter be constructed?
        """
        MarkdownImporter()


    def test_import(self):
        """
        Can a MarkdownExporter export something?
        """
        (output, resources) = (MarkdownImporter()
            .from_filename(
                os.path.join(
                    os.path.dirname(__file__),
                    "files",
                    "notebook1.md")
            )
        )
        assert len(output) > 0