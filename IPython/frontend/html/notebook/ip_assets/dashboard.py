from flask.ext.assets import Bundle

scripts = Bundle(
    'js/notebooklist.js',
    'js/clusterlist.js',
    'js/projectdashboardmain.js',
    filters='rjsmin',
    output='db.min.js')

styles = Bundle(
    'css/alternateuploadform.css',
    'css/style.min.css',
    'css/projectdashboard.css',
    output='db.min.css'
)
