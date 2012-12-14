//----------------------------------------------------------------------------
//  Copyright (C) 2012  Nicholas Bollweg
//
//  Distributed under the terms of the Apache License.  The full license is in
//  the file COPYING, distributed as part of this software.
//----------------------------------------------------------------------------

//============================================================================
// BlocklyCell
//============================================================================
/**
 * An extendable module that provide base functionnality to create cell for notebook.
 * @module IPython-Blockly
 * @namespace IPython-Blockly
 * @submodule BlocklyCell
 */

var IPython = (function (IPython) {
    "use strict";

    var utils = IPython.utils;
    var key   = IPython.utils.keycodes;
    
    /**
     * A Cell conceived to write code visually.
     *
     * The kernel doesn't have to be set at creation time, in that case
     * it will be null and set_kernel has to be called later.
     * @class BlocklyCell
     * @extends IPython.CodeCell
     *
     * @constructor
     * @param {Object|null} kernel
     */
    var BlocklyCell = function (kernel) {
        this.kernel = kernel || null;
        this.code_mirror = null;
        this.input_prompt_number = null;
        this.tooltip_on_tab = true;
        this.collapsed = false;
        this.default_mode = 'python';
        IPython.Cell.apply(this, arguments);

        var that = this;
        this.element.focusout(
            function() { that.auto_highlight(); }
        );
    };
    

    IPython.register_celltype("blockly", BlocklyCell, {
        construct: function(kernel){
            var cell = new BlocklyCell(kernel);
            cell.set_input_prompt();
            return cell;
        }});
    
    IPython.BlocklyCell = BlocklyCell;

    return IPython;
}(IPython));