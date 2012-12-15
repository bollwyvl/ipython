;(function(){
    function blockly_handler(json, element){
        element.append($("<img/>", {
            src: "http://blockly.googlecode.com/svn/wiki/sample.png"
        }));
    }
    IPython.json_handlers.register_handler('blockly', blockly_handler);
})();