'''
An experimental Flask implementation of the IPython Web Notebook
'''
from flask import (
    Flask,
    render_template,
)

from flask.ext.assets import Environment, Bundle

def make_app(ip_app, handler):
    
    app = Flask(__name__)
    assets = Environment(app)
    assets.register('notebook_js', notebook_js)
    
    @app.route('/<notebook_id>')
    def index(notebook_id):
        nbm = ip_app.notebook_manager
        project = nbm.notebook_dir
        
        if not nbm.notebook_exists(notebook_id):
            return u'Notebook does not exist: %s' % notebook_id, 404
        
        ctxt = dict(
            project=project,
            notebook_id=notebook_id,
            base_project_url=ip_app.ipython_app.base_project_url,
            base_kernel_url=ip_app.ipython_app.base_kernel_url,
            kill_kernel=False,
            read_only=ip_app.read_only,
            logged_in=handler.logged_in,
            login_available=handler.login_available,
            mathjax_url=ip_app.ipython_app.mathjax_url,
            use_less=ip_app.use_less
        )
        
        return render_template('notebook.html', **ctxt)
    
    return app

notebook_js = Bundle(
    'codemirror/lib/codemirror.js',
    'codemirror/lib/util/loadmode.js',
    'codemirror/lib/util/multiplex.js',
    'codemirror/mode/python/python.js',
    'codemirror/mode/htmlmixed/htmlmixed.js',
    'codemirror/mode/xml/xml.js',
    'codemirror/mode/javascript/javascript.js',
    'codemirror/mode/css/css.js',
    'codemirror/mode/rst/rst.js',
    'codemirror/mode/markdown/markdown.js',

    'pagedown/Markdown.Converter.js',

    'prettify/prettify.js',
    'dateformat/date.format.js',

    'js/events.js',
    'js/utils.js',
    'js/layoutmanager.js',
    'js/mathjaxutils.js',
    'js/outputarea.js',
    'js/cell.js',
    'js/celltoolbar.js',
    'js/codecell.js',
    'js/completer.js',
    'js/textcell.js',
    'js/kernel.js',
    'js/savewidget.js',
    'js/quickhelp.js',
    'js/pager.js',
    'js/menubar.js',
    'js/toolbar.js',
    'js/maintoolbar.js',
    'js/notebook.js',
    'js/notificationwidget.js',
    'js/notificationarea.js',
    'js/tooltip.js',
    'js/config.js',
    'js/notebookmain.js',

    'js/contexthint.js',

    'js/celltoolbarpresets/default.js',
    'js/celltoolbarpresets/slideshow.js',
    filters='rjsmin',
    output='static/notebook.min.js')