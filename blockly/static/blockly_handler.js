;(function(){
    function blockly_handler(json, element){
        var id = 'blockly-' + IPython.utils.uuid(),
            toinsert = $("<div/>").attr('id', id);
        
        var x = $(
            '<xml id="startBlocks" style="display: none">' +
            '    <block type="controls_if" inline="false" x="-100" y="50">' +
            '      <value name="IF0">' +
            '        <block type="logic_compare" inline="true">' +
            '          <title name="OP">LT</title>' +
            '          <value name="A">' +
            '            <block type="variables_get">' +
            '              <title name="VAR">item</title>' +
            '            </block>' +
            '          </value>' +
            '          <value name="B">' +
            '            <block type="math_number">' +
            '              <title name="NUM">256</title>' +
            '            </block>' +
            '          </value>' +
            '        </block>' +
            '      </value>' +
            '      <statement name="DO0">' +
            '        <block type="variables_set" inline="false">' +
            '          <title name="VAR">item</title>' +
            '          <value name="VALUE">' +
            '            <block type="math_number">' +
            '              <title name="NUM">0</title>' +
            '            </block>' +
            '          </value>' +
            '          <next>' +
            '            <block type="text_print" inline="false">' +
            '              <value name="TEXT">' +
            '                <block type="text">' +
            '                  <title name="TEXT">Game Over</title>' +
            '                </block>' +
            '              </value>' +
            '            </block>' +
            '          </next>' +
            '        </block>' +
            '      </statement>' +
            '    </block>' +
            '  </xml>'
        );

        element.append(x);
        element.append(toinsert);
        
        Blockly.inject(toinsert[0], {path: '/static/jsplugins/blockly/'});
                
        Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, x[0]);
    }
    
    IPython.json_handlers.register_handler('blockly', blockly_handler);
})();