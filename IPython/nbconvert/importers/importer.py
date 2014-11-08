"""This module defines a base Exporter class. For Jinja template-based export,
see templateexporter.py.
"""


from __future__ import print_function, absolute_import

import io
import os
import copy
import collections
import datetime

from IPython.config.configurable import LoggingConfigurable
from IPython.config import Config
from IPython import nbformat
from IPython.utils.traitlets import MetaHasTraits, Unicode, List
from IPython.utils.importstring import import_item
from IPython.utils import text, py3compat


class ResourcesDict(collections.defaultdict):
    def __missing__(self, key):
        return ''


class Importer(LoggingConfigurable):
    
    encoding = 'utf-8'
    
    def from_filename(self, filename, resources=None, **kw):
        """
        Convert a text file to a notebook node. Return a filename.
        
        Override this to handle a binary file.

        Parameters
        ----------
        filename : str
            Full filename of the file to open and convert.
        """

        # Pull the metadata from the filesystem.
        if resources is None:
            resources = ResourcesDict()
        if not 'metadata' in resources or resources['metadata'] == '':
            resources['metadata'] = ResourcesDict()
        basename = os.path.basename(filename)
        notebook_name = basename[:basename.rfind('.')]
        resources['metadata']['name'] = notebook_name

        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        resources['metadata']['modified_date'] = modified_date.strftime(text.date_format)

        with io.open(filename, encoding=self.encoding) as f:
            content = f.read()
        return self.to_notebook_node(content, resources=resources, **kw)
        
        