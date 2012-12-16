import os
import shutil
import fnmatch
import time

from zmq.utils import jsonapi

_loaded = False

class Blockly(object):
    def __init__(self, height=500):
        self.height = height
        
    def __repr__json__(self):
        """
        would this be called anyway without adding the handler?
        """
        return jsonapi.dumps(dict(
            handler = "blockly",
            height = self.height
        ))

def copy_assets(ip):
    opj = os.path.join
    
    module_root = os.path.dirname(__file__)
    static_dest = opj(ip.profile_dir.location, "static", "jsplugins", "blockly")
    blkly_root = opj(module_root, "vendor", "blockly")
    blkly_dest = opj(static_dest, "blockly")
    
    assets = {
        (module_root, "static"): (
            "*",
                opj(static_dest)),
        (blkly_root, "demos"): (
            "blockly_compressed.js",
                blkly_dest),
        # OOH, you terrible beast. the XXX makes it load later.
        (blkly_root, "language", "common"): (
            "*",
                opj(blkly_dest, "language", "common")),
        (blkly_root, "language", "en"): (
            "*",
                opj(blkly_dest, "language", "en")),
        (blkly_root, "generators"): (
            "python.js",
                opj(blkly_dest, "generators")),
        (blkly_root, "generators", "python"): (
            "*",
                opj(blkly_dest, "generators", "python")),
        (blkly_root, "media"): (
            "*",
                opj(blkly_dest, "media")),
    }
    
    shutil.rmtree(static_dest, ignore_errors=True)
    
    for src, what_where in assets.items():
        what, where = what_where
        if not os.path.exists(where):
            os.makedirs(where)
        for root, dirnames, filenames in os.walk(opj(*src)):
            for filename in fnmatch.filter(filenames, what):
                shutil.copy(opj(root, filename), where)

    print "If this is the first time you have used ipython-blockly, or you are a developer and have added/deleted assets files, you must restart your notebook web application... not just reload the page! %s" % time.time()

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    
    
    if not _loaded:
        json_formatter = ip.display_formatter.formatters['application/json']

        json_formatter.for_type_by_name(
            __name__, Blockly.__name__, lambda blkly: blkly.__repr__json__()
        )
        _loaded = True
        
    copy_assets(ip)
