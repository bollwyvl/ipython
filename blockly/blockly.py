import os

from IPython.frontend.html.notebook.extensions import IPythonNotebookExtension

# TODO: create a base class someplace 
class BlocklyNotebookExtension(IPythonNotebookExtension):
    def __init__(self, *args, **kwargs):
        super(BlocklyNotebookExtension, self).__init__(*args, **kwargs)
        
        self.static_paths = [
            os.path.join(os.path.dirname(__file__), "static"),
        ]
    
        self.assets = [
            "blockly/blockly.js",
            "blockly/blocklycell.js",
            "blockly/blockly.css",
        ]