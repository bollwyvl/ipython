"""Base TestCase class for testing Exporters"""

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

from ...tests.base import TestsBase

#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

all_raw_mimetypes = {
    'text/x-python',
    'text/markdown',
    'text/html',
    'text/restructuredtext',
    'text/latex',
}

class ImportersTestsBase(TestsBase):
    """Contains base test functions for importers"""
    
    importer_class = None