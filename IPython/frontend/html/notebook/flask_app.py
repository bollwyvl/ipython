"""
An experimental Flask implementation of the IPython Web Notebook
"""
from flask import (
    Flask,
    render_template,
)

from flask.ext.assets import Environment

def make_app(ip_app, **handlers):
    """
    factory-style app builder
    """
    app = Flask(__name__)

    # set up assets
    assets = Environment(app)
    register_assets(assets)

    # views ###################################################################
    @app.route('/', methods=['GET'])
    def dashboard():
        ctxt = base_ctxt(handlers["dashboard"])
        
        ctxt.update(dict(
            project_component=ctxt["project"].split('/'),
        ))
        
        return render_template('projectdashboard.html', **ctxt)
    
    @app.route('/<notebook_id>', methods=['GET'])
    def notebook(notebook_id):
        """
        serves up the randomly-renamed notebook
        """
        if not nbm().notebook_exists(notebook_id):
            return u'Notebook does not exist: %s' % notebook_id, 404

        ctxt = base_ctxt(handlers["notebook"])

        ctxt.update(dict(
            notebook_id=notebook_id,
            kill_kernel=False,
        ))

        return render_template('notebook.html', **ctxt)


    # helpers #################################################################
    def base_ctxt(handler):
        """
        a DRY thingy for commonly-used template variables
        """
        return dict(
            project=nbm().notebook_dir,
            base_project_url=ip_app.ipython_app.base_project_url,
            base_kernel_url=ip_app.ipython_app.base_kernel_url,
            logged_in=handler.logged_in,
            login_available=handler.login_available,
            read_only=ip_app.read_only,
            use_less=ip_app.use_less,
            mathjax_url=ip_app.ipython_app.mathjax_url,
        )

    def nbm():
        """
        a DRY thingy for getting to the notebook manager
        """
        return ip_app.notebook_manager

    # the app which will be WSGIContainer'd ###################################
    return app


def register_assets(assets):
    """
    handle webassets
    """
    from ip_assets import (
        notebook,
        dashboard
    )
    
    assets.register('notebook_js', notebook.scripts)
    assets.register('notebook_css', notebook.styles)
    
    assets.register('dashboard_js', dashboard.scripts)
    assets.register('dashboard_css', dashboard.styles)

