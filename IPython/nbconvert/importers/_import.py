"""Module containing single call import functions."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from functools import wraps

from IPython.nbformat import NotebookNode
from IPython.utils.decorators import undoc
from IPython.utils.py3compat import string_types

from .importer import Importer
from .markdown import MarkdownImporter

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

@undoc
def DocDecorator(f):
    
    #Set docstring of function
    f.__doc__ = f.__doc__ + """
    nb : :class:`~IPython.nbformat.NotebookNode`
      The object to import.
    config : config (optional, keyword arg)
        User configuration instance.
    resources : dict (optional, keyword arg)
        Resources used in the conversion process.
        
    Returns
    -------
    tuple- output, resources, importer_instance
    output : str
        Jinja 2 output.  This is the resulting converted notebook.
    resources : dictionary
        Dictionary of resources used prior to and during the conversion 
        process.
    importer_instance : Importer
        Instance of the Importer class used to import the document.  Useful
        to caller because it provides a 'file_extension' property which
        specifies what extension the output should be saved as.

    Notes
    -----
    WARNING: API WILL CHANGE IN FUTURE RELEASES OF NBCONVERT
    """
            
    @wraps(f)
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorator


#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

__all__ = [
    '_import',
    'import_markdown',
    'import_by_name',
    'get_import_names',
    'ImporterNameError'
]


class ImporterNameError(NameError):
    pass

@DocDecorator
def _import(importer, nb, **kw):
    """
    Import an input to a notebook object using specific importer class.
    
    Parameters
    ----------
    importer : class:`~IPython.nbconvert.importers.importer.Importer` class or instance
      Class type or instance of the importer that should be used.  If the
      method initializes it's own instance of the class, it is ASSUMED that
      the class type provided exposes a constructor (``__init__``) with the same
      signature as the base Importer class.
    """
    
    #Check arguments
    if importer is None:
        raise TypeError("Importer is None")
    elif not isinstance(importer, Importer) and not issubclass(importer, Importer):
        raise TypeError("importer does not inherit from Importer (base)")
    if nb is None:
        raise TypeError("nb is None")
    
    #Create the importer
    resources = kw.pop('resources', None)
    if isinstance(importer, Importer):
        importer_instance = importer
    else:
        importer_instance = importer(**kw)
    
    #Try to convert the notebook using the appropriate conversion function.
    if isinstance(nb, NotebookNode):
        output, resources = importer_instance.from_notebook_node(nb, resources)
    elif isinstance(nb, string_types):
        output, resources = importer_instance.from_filename(nb, resources)
    else:
        output, resources = importer_instance.from_file(nb, resources)
    return output, resources

importer_map = dict(
    markdown=MarkdownImporter,
)

def _make_importer(name, E):
    """make an import_foo function from a short key and Importer class E"""
    def _import(nb, **kw):
        return _import(E, nb, **kw)
    _import.__doc__ = """Import a {0} object to notebook format""".format(name)
    return _import
    
g = globals()

for name, E in importer_map.items():
    g['import_%s' % name] = DocDecorator(_make_importer(name, E))

@DocDecorator
def import_by_name(format_name, nb, **kw):
    """
    Import an object type by its name to a notebook.  Reflection
    (Inspect) is used to find the template's corresponding explicit import
    method defined in this module.  That method is then called directly.
    
    Parameters
    ----------
    format_name : str
        Name of the template style to import to.
    """
    
    function_name = "import_" + format_name.lower()
    
    if function_name in globals():
        return globals()[function_name](nb, **kw)
    else:
        raise ImporterNameError("template for `%s` not found" % function_name)


def get_import_names():
    """Return a list of the currently supported import targets

    WARNING: API WILL CHANGE IN FUTURE RELEASES OF NBCONVERT"""
    return sorted(importer_map.keys())
