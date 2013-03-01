from flask import (
    Flask,
    render_template,
)

def make_app(ip_app, handler):
    
    app = Flask(__name__,
        
    )
    
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
        
        return render_template("notebook.html", **ctxt)
    
    return app