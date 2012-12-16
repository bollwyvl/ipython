import os
import shutil
import fnmatch

from zmq.utils import jsonapi

_loaded = False

class Blockly(object):
    pass

def blockly_to_json(B):
    d = {}
    d['handler'] = 'blockly'
    return jsonapi.dumps(d)

def copy_assets(ip):
    opj = os.path.join
    
    module_root = os.path.dirname(__file__)
    static_dest = opj(ip.profile_dir.location, "static", "jsplugins", "blockly")
    blkly_root = opj(module_root, "vendor", "blockly")
    blkly_dest = opj(static_dest, "blockly")
    
    assets = {
        (module_root, "static"): (
            "*",
                opj(static_dest, "XXX")),
        (blkly_root, "demos"): (
            "blockly_compressed.js",
                blkly_dest),
        # OOH, you terrible beast. the XXX makes it load later.
        (blkly_root, "language", "common"): (
            "*",
                opj(blkly_dest, "language", "XXXcommon")),
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
        
    #
    #shutil.copytree(blockly_static, profile_static)


    #print(" ".join(["copied", blockly_static, "to", profile_static]))
    print "If this is the first time you have used blockly, or you are a developer and have added/deleted assets files, you must restart your notebook web application... not just reload the page!"

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    
    
    if not _loaded:
        json_formatter = ip.display_formatter.formatters['application/json']

        json_formatter.for_type_by_name(
            __name__, Blockly.__name__, blockly_to_json
        )
        _loaded = True
        
    copy_assets(ip)
