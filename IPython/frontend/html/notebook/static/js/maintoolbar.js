//----------------------------------------------------------------------------
//  Copyright (C) 2011 The IPython Development Team
//
//  Distributed under the terms of the BSD License.  The full license is in
//  the file COPYING, distributed as part of this software.
//----------------------------------------------------------------------------

//============================================================================
// ToolBar
//============================================================================

var IPython = (function (IPython) {

    var MainToolBar = function (selector) {
        this.selector = selector;
        IPython.ToolBar.apply(this, arguments);
        this.construct();
        this.add_drop_down_list();
        this.bind_events();
    };

    MainToolBar.prototype = new IPython.ToolBar(); 

    MainToolBar.prototype.construct = function () {
        this.add_buttons_group([
                {
                    id : 'save_b',
                    label : 'Save',
                    icon : 'ui-icon-disk',
                    callback : function () {
                        IPython.notebook.save_notebook();
                        }
                }
            ]);
        this.add_buttons_group([
                {
                    id : 'cut_b',
                    label : 'Cut Cell',
                    icon : 'ui-icon-scissors',
                    callback : function () {
                        IPython.notebook.cut_cell();
                        }
                },
                {
                    id : 'copy_b',
                    label : 'Copy Cell',
                    icon : 'ui-icon-copy',
                    callback : function () {
                        IPython.notebook.copy_cell();
                        }
                },
                {
                    id : 'paste_b',
                    label : 'Paste Cell Below',
                    icon : 'ui-icon-clipboard',
                    callback : function () {
                        IPython.notebook.paste_cell_below();
                        }
                }
            ],'cut_copy_paste');

        this.add_buttons_group([
                {
                    id : 'move_up_b',
                    label : 'Move Cell Up',
                    icon : 'ui-icon-arrowthick-1-n',
                    callback : function () {
                        IPython.notebook.move_cell_up();
                        }
                },
                {
                    id : 'move_down_b',
                    label : 'Move Cell Down',
                    icon : 'ui-icon-arrowthick-1-s',
                    callback : function () {
                        IPython.notebook.move_cell_down();
                        }
                }
            ],'move_up_down');
        
        this.add_buttons_group([
                {
                    id : 'insert_above_b',
                    label : 'Insert Cell Above',
                    icon : 'ui-icon-arrowthickstop-1-n',
                    callback : function () {
                        IPython.notebook.insert_cell_above('code');
                        }
                },
                {
                    id : 'insert_below_b',
                    label : 'Insert Cell Below',
                    icon : 'ui-icon-arrowthickstop-1-s',
                    callback : function () {
                        IPython.notebook.insert_cell_below('code');
                        }
                }
            ],'insert_above_below');

        this.add_buttons_group([
                {
                    id : 'run_b',
                    label : 'Run Cell',
                    icon : 'ui-icon-play',
                    callback : function () {
                    IPython.notebook.execute_selected_cell();
                        }
                },
                {
                    id : 'interrupt_b',
                    label : 'Interrupt',
                    icon : 'ui-icon-stop',
                    callback : function () {
                        IPython.notebook.kernel.interrupt();
                        }
                }
            ],'run_int');


    };

    MainToolBar.prototype.add_drop_down_list = function () {
        var select = $('<select/>')
                .attr('id','cell_type')
                .addClass('ui-widget ui-widget-content')

        console.log(IPython.registered_celltypes())
        
        $.each(IPython.registered_celltypes(), function(idx, cell_type){
            $.each(cell_type.buttons, function(idx, btn){
                select
                    .append(
                        $('<option/>')
                            .attr('value', btn.value)
                            .text(btn.text)
                    );
            });
        });
        
        $(this.selector).append(select);
    };

    MainToolBar.prototype.bind_events = function () {
        var that = this;
        
        this.element.find('#cell_type').change(function () {
            var cell_type = [undefined].concat($(this).val().split(" "));
            
            IPython.notebook.to_cell_type.apply(
                IPython.notebook,
                cell_type);
        });
        
        $([IPython.events]).on('selected_cell_type_changed.Notebook', function (event, data) {
            if (data.cell_type === 'heading') {
                that.element.find('#cell_type').val(data.cell_type+data.level);
            } else {
                that.element.find('#cell_type').val(data.cell_type);
            }
        });
    };

    IPython.MainToolBar = MainToolBar;

    return IPython;

}(IPython));
