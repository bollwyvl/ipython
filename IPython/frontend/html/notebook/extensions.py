from pkg_resources import iter_entry_points

import itertools

entry_points = {}

def initialize():
    global entry_points
    entry_points = dict(
        [(ep.name, ep.load()()) for ep in iter_entry_points("ipnotebook")]
    )

def static_paths(def_paths):
    result = def_paths
    if isinstance(def_paths, basestring) or isinstance(def_paths, unicode):
        result = [result]
    return list(itertools.chain.from_iterable([
        ext.static_paths for ext in entry_points.values() 
    ])) + result

def assets():
    # TODO: what about dependencies
    return list(itertools.chain.from_iterable([
        ext.assets for ext in entry_points.values() 
    ]))

class IPythonNotebookExtension(object):
    def __init__(self):
        self.static_paths = []
        self.assets = []
    