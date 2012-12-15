import os
import shutil
    
from zmq.utils import jsonapi

_loaded = False

class Blockly(object):
    pass

def blockly_to_json(B):
    d = {}
    d['handler'] = 'blockly'
    return jsonapi.dumps(d)

def load_ipython_extension(ip):
    """Load the extension in IPython."""

    global _loaded
    if not _loaded:
        json_formatter = ip.display_formatter.formatters['application/json']

        json_formatter.for_type_by_name(
            __name__, Blockly.__name__, blockly_to_json
        )
        _loaded = True
        
        print("""loaded blockly handler...""")
        blockly_static = os.path.join(os.path.dirname(__file__), "static")
        profile_static = os.path.join(ip.profile_dir.location, "static",
                "jsplugins",
                "blockly")

        shutil.rmtree(profile_static, ignore_errors=True)
        shutil.copytree(blockly_static, profile_static)
        print(" ".join(["copied", blockly_static, "to", profile_static]))
        print "If this is the first time you have used blockly, you must restart your notebook (not just reload the page)"
