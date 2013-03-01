from flask.ext.assets import Bundle

scripts = Bundle(
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
    output='nb.min.js')

styles = Bundle(
    'codemirror/lib/codemirror.css',
    'css/codemirror-ipython.css',
    'prettify/prettify.css',
    'css/celltoolbar.css',
    output='nb.min.css'
)