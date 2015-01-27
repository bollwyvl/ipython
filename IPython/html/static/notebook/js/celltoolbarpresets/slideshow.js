// Copyright (c) IPython Development Team.
// Distributed under the terms of the Modified BSD License.

define([
    'jquery',
    'underscore',
    'notebook/js/celltoolbar',
    'notebook/js/toolbar',
    'base/js/events',
    'base/js/namespace',
], function($, _, celltoolbar, toolbar, events, IPython) {
    "use strict";

    var CellToolbar = celltoolbar.CellToolbar;

    var preset_name = "Slideshow";
    var slideshow_preset = [];

    var slideshow_toolbar;

    var SlideshowToolBar = function (selector, options) {
        /**
         * Constructor
         *
         * Parameters:
         *  selector: string
         *  options: dictionary
         *      Dictionary of keyword arguments.
         *          events: $(Events) instance
         *          notebook: Notebook instance
         **/
        toolbar.ToolBar.apply(this, [selector, options]);

        this.events = options.events;
        this.notebook = options.notebook;

        this._init_metadata()
            ._init_events()
            ._init_actions()
            ._make()
            ._init_extras();

        this.notebook.keyboard_manager.register_events(this.element);


        Object.seal(this);
    };

    SlideshowToolBar.prototype = Object.create(toolbar.ToolBar.prototype);

    SlideshowToolBar._bootstrap = function(event, data){
        if(IPython.slideshow_toolbar || data.name !== preset_name){
            return;
        }

        $("#maintoolbar-container").after($("<div/>", {
            id: "slideshowtoolbar-container",
            "class": "container toolbar"
        }));

        IPython.slideshow_toolbar = new SlideshowToolBar(
            '#slideshowtoolbar-container',
            {
                notebook: IPython.notebook,
                events: events,
                actions: IPython.toolbar.actions
            }
        );
    };

    SlideshowToolBar.prototype.list_themes = function () {
        return {
            "": "Default",
            beige: "Beige",
            blood: "Blood",
            moon: "Moon",
            night: "Night",
            serif: "Serif",
            simple: "Simple",
            sky: "Sky",
            solarized: "Solarized"
        };
    };

    SlideshowToolBar.prototype.list_transitions = function () {
        return {
            "": "Default",
            cube: "Cube",
            page: "Page",
            concave: "Concave",
            zoom: "Zoom",
            linear: "Linear",
            fade: "Fade",
            none: "None"
        };
    };

    SlideshowToolBar.prototype.list_transition_speeds = function () {
        return {
            "": "Default",
            fast: "Fast",
            slow: "Slow"
        };
    };

    SlideshowToolBar.prototype.list_view_distances = function () {
        return _.range(9).reduce(function(memo, i){
            memo[i] = i;
            return memo;
        }, {});
    };

    SlideshowToolBar.prototype._init_metadata = function () {
        if(!this.notebook.metadata.hasOwnProperty("slideshow")){
            this.notebook.metadata.slideshow = {};
        }

        return this;
    };


    SlideshowToolBar.prototype._init_events = function() {
        var that = this;

        this.events.on({
            "preset_activated.CellToolbar": function(event, data){
                return that.visible(data.name === preset_name);
            },
            "unregistered_preset.CellToolbar": function(event, data){
                return that.visible(data.name !== preset_name);
            }
        });

        return this;
    };


    SlideshowToolBar.reveal_config_defaults = function(){
        return {

            // Display controls in the bottom right corner
            controls: true,

            // Display a presentation progress bar
            progress: true,

            // Display the page number of the current slide
            slideNumber: false,

            // Push each slide change to the browser history
            history: false,

            // Enable keyboard shortcuts for navigation
            keyboard: true,

            // Enable the slide overview mode
            overview: true,

            // Vertical centering of slides
            center: true,

            // Enables touch navigation on devices with touch input
            touch: true,

            // Loop the presentation
            loop: false,

            // Change the presentation direction to be RTL
            rtl: false,

            // Turns fragments on and off globally
            fragments: true,

            // Flags if the presentation is running in an embedded mode,
            // i.e. contained within a limited portion of the screen
            embedded: false,

            // Flags if we should show a help overlay when the questionmark
            // key is pressed
            help: true,

            // Number of milliseconds between automatically proceeding to the
            // next slide, disabled when set to 0, this value can be overwritten
            // by using a data-autoslide attribute on your slides
            autoSlide: 0,

            // Stop auto-sliding after user input
            autoSlideStoppable: true,

            // Enable slide navigation via mouse wheel
            mouseWheel: false,

            // Hides the address bar on mobile devices
            hideAddressBar: true,

            // Opens links in an iframe preview overlay
            previewLinks: false,

            // Transition style
            transition: 'default', // none/fade/slide/convex/concave/zoom

            // Transition speed
            transitionSpeed: 'default', // default/fast/slow

            // Transition style for full page slide backgrounds
            backgroundTransition: 'default', // none/fade/slide/convex/concave/zoom

            // Number of slides away from the current that are visible
            viewDistance: 3,

            // Parallax background image
            parallaxBackgroundImage: '', // e.g. "'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg'"

            // Parallax background size
            parallaxBackgroundSize: '' // CSS syntax, e.g. "2100px 900px"


        };
    };


    SlideshowToolBar.prototype._init_actions = function () {
        var that = this;

        var _make_toggle = function(key){
            return function(env){
                var meta = env.notebook.metadata.slideshow;
                meta[key] = !meta[key];
            };
        };

        this._slideshow_actions = {
            show_controls: {
                icon: "fa-arrows",
                help: "Display controls in the bottom right corner",
                handler: _make_toggle("controls"),
                default_value: true,
                toggle: true
            },
            show_progress: {
                icon: "fa-star-half-o",
                help: "Display a presentation progress bar",
                handler: _make_toggle("progress"),
                default_value: true,
                toggle: true
            },
            show_slide_number: {
                icon: "fa-subscript",
                help: "Display the page number of the current slide",
                handler: _make_toggle("slideNumber"),
                default_value: false,
                toggle: true
            },
            push_history: {
                icon: "fa-history",
                help: "Push each slide change to the browser history",
                handler: _make_toggle("history"),
                default_value: false,
                toggle: true
            },
            enable_keyboard: {
                icon: "fa-keyboard-o",
                help: "Enable keyboard shortcuts for navigation",
                handler: _make_toggle("keyboard"),
                default_value: true,
                toggle: true
            },
            enable_overview: {
                icon: "fa-sitemap",
                help: "Enable the slide overview mode",
                handler: _make_toggle("overview"),
                default_value: true,
                toggle: true
            },
            center_slides: {
                icon: "fa-align-center fa-rotate-90",
                help: "Vertical centering of slides",
                handler: _make_toggle("center"),
                default_value: true,
                toggle: true
            },
            enable_touch: {
                icon: "fa-hand-o-up",
                help: "Enables touch navigation on devices with touch input",
                handler: _make_toggle("touch"),
                default_value: true,
                toggle: true
            },
            enable_loop: {
                icon: "fa-repeat",
                help: "Loop the presentation",
                handler: _make_toggle("loop"),
                default_value: false,
                toggle: true
            },
            right_to_left: {
                icon: "fa-align-right",
                help: "Change the presentation direction to be RTL",
                handler: _make_toggle("rtl"),
                default_value: false,
                toggle: true
            },
            enable_fragments: {
                icon: "fa-tasks",
                help: "Turns fragments on and off globally",
                handler: _make_toggle("fragments"),
                default_value: true,
                toggle: true
            },
            enable_embedded: {
                icon: "fa-indent",
                help: "Flags if the presentation is running in an embedded mode",
                handler: _make_toggle("embedded"),
                default_value: false,
                toggle: true
            },
            enable_help: {
                icon: "fa-life-ring",
                help: "Flags if we should show a help overlay when the questionmark key is pressed",
                handler: _make_toggle("help"),
                default_value: false,
                toggle: true
            },
            // TODO: autoslide?
            enable_autoslide_stop: {
                icon: "fa-cab",
                help: "Stop auto-sliding after user input",
                handler: _make_toggle("autoSlideStoppable"),
                default_value: true,
                toggle: true
            },
            enable_mouse_wheel: {
                icon: "fa-sort",
                help: "Enable slide navigation via mouse wheel",
                handler: _make_toggle("mouseWheel"),
                default_value: false,
                toggle: true
            },
            show_addressbar: {
                icon: "fa-terminal",
                help: "Hides the address bar on mobile devices",
                handler: _make_toggle("hideAddressBar"),
                default_value: true,
                toggle: true
            },
            enable_link_preview: {
                icon: "fa-share-square",
                help: "Opens links in an iframe preview overlay",
                handler: _make_toggle("previewLinks"),
                default_value: false,
                toggle: true
            }
        };

        $.each(this._slideshow_actions, function(key, action){
            that.actions.register(action, key, "slideshow");
        });

        return this;
    };

    SlideshowToolBar.prototype._init_extras = function () {
        var el = this.element;
        var meta = this.notebook.metadata.slideshow;

        $.each(this._slideshow_actions, function(key, action){
            if(action.toggle){
                el.find("[data-jupyter-action='slideshow." + key +"']")
                    .attr({
                        "data-toggle": "button"
                    })
                    .toggleClass("active",
                        (key in meta) ? !!meta[key] : action.default_value
                    );
            }
        });

        return this;
    };

    SlideshowToolBar.prototype._make = function () {
        var grps = [
            ['<add_slideshow_themes>'],
            ['<add_slideshow_transitions>'],
            ['<add_slideshow_transition_speeds>'],
            ['<add_slideshow_view_distances>'],
            [
                [
                    'slideshow.show_controls',
                    'slideshow.show_progress',
                    'slideshow.show_slide_number',
                    'slideshow.show_addressbar',
                    'slideshow.center_slides',
                    'slideshow.right_to_left'
                ], 'visual'
            ],
            [
                [
                    'slideshow.push_history',
                    'slideshow.enable_keyboard',
                    'slideshow.enable_touch',
                    'slideshow.enable_mouse_wheel',
                    'slideshow.enable_overview',
                    'slideshow.enable_link_preview',
                    'slideshow.enable_help'
                ], 'ui_features'
            ],
            [
                [
                    'slideshow.enable_loop',
                    'slideshow.enable_fragments',
                    'slideshow.enable_embedded'
                ], 'playback'
            ],
            ['<add_slideshow_autoslide>']
        ];
        this.construct(grps);

        return this;
    };

    SlideshowToolBar.prototype._make_selector = function(key, items, options){
        var that = this;
        var dropdown = $("<div/>", {
            "class": "dropdown",
            title: options.help
        });
        var label = $("<span/>")
            .text(items[this.notebook.metadata.slideshow[key]]);
        var button = $("<button/>",
                {
                    "class": "btn btn-default dropdown-toggle",
                    type: "button",
                    "data-toggle": "dropdown"
                })
                .append(
                    $("<i/>", {"class": "fa fa-fw " + options.icon}),
                    label,
                    $("<span/>").html("&nbsp;"),
                    $("<span/>", {"class": "caret"}))
                .appendTo(dropdown);

        var list = $("<ul/>", {
                "class": "dropdown-menu",
                "role": "menu"
            })
            .appendTo(dropdown);

        if(options.label){
            list.append($("<li/>", {"class": "dropdown-header"})
                .text(options.label));
        }

        $.each(items, function(item, name){
            list.append($('<li/>', {
                role: "presentation"
            }).append($("<a/>", {
                    role: "menuitem",
                    tabindex: -1
                })
                .text(name).click(function(){
                    if (!item) {
                        delete that.notebook.metadata.slideshow[key];
                    } else {
                        that.notebook.metadata.slideshow[key] = item;
                    }
                    label.text(name);
                })));
        });

        return $('<div/>', {"class": "btn-group"}).append(dropdown);
    };

    SlideshowToolBar.prototype._pseudo_actions.add_slideshow_themes = function () {
        return this._make_selector("theme", this.list_themes(), {
            label: "Themes",
            icon: "fa-paint-brush",
            help: "Slideshow theme"
        });
    };

    SlideshowToolBar.prototype._pseudo_actions.add_slideshow_autoslide = function () {
        var that = this;
        var meta = this.notebook.metadata.slideshow;

        var grp = $("<div/>", {"class": "input-group input-group-sm"});
        var grp_btn = $("<div/>", {"class": "input-group-btn"})
            .appendTo(grp);

        var btn_style = {
            height: 24,
            width: 29,
            padding: "0 5px 0 5px"
        };

        var enable_btn = $("<button/>", {
                "class": "btn btn-default" + (
                    "autoSlide" in meta ? " active" : ""
                ),
                "data-toggle": "button",
                "title": "automatically advance slides"
            })
            .css(btn_style)
            .append($("<i/>", {"class": "fa fa-car"}))
            .appendTo(grp_btn)
            .on("click", function(){
                if("autoSlide" in meta){
                    delete meta.autoSlide;
                    ms_label.hide();
                    input.hide();
                    stop_btn.hide();
                }else{
                    meta.autoSlide = 0;
                    ms_label.show();
                    input.show();
                    stop_btn.show();
                }
            });


        var input = $("<input/>", {
                "class": "form-control",
                type: "number",
                value: "autoSlide" in meta ? meta.autoSlide : "",
                title: "Number of milliseconds between automatically proceeding to the next slide, disabled when set to 0, this value can be overwritten by using a `data-autoslide` attribute on your slides"
            })
            .css({
                height: 24,
                width: 60,
                "text-align": "right",
                padding: "0 0 0 0",
                display: "autoSlide" in meta ? "inherit" : "none"
            })
            .appendTo(grp)
            .on("input", function(){
                meta.autoSlide = parseInt(input.val());
            });

        var ms_label = $("<span/>", {
                "class": "input-group-addon"
            })
            .text("ms")
            .css(btn_style)
            .css({
                display: "autoSlide" in meta ? "inherit" : "none"
            })
            .appendTo(grp);

        var stop_btn = $("<button/>", {
                "class": "btn btn-default " + (
                    !("autoSlideStoppable" in meta) ||
                        meta.autoSlideStoppable ? "active" : ""
                ),
                "data-toggle": "button",
                title: "Stop auto-sliding after user input"
            })
            .css(btn_style)
            .css({
                display: "autoSlide" in meta ? "inherit" : "none"
            })
            .append($("<i/>", {"class": "fa fa-fire-extinguisher"}))
            .appendTo(grp)
            .on("click", function(){
                meta.autoSlideStoppable = !meta.autoSlideStoppable;
            });

        return $("<span/>",{"class": "navbar-form btn-group"})
            .append(grp);
    };

    SlideshowToolBar.prototype._pseudo_actions.add_slideshow_transitions = function () {
        return this._make_selector("transition", this.list_transitions(), {
            label: "Transitions",
            icon: "fa-exchange",
            help: "Transition style"
        });
    };

    SlideshowToolBar.prototype._pseudo_actions.add_slideshow_transition_speeds = function () {
        return this._make_selector("transitionSpeed", this.list_transition_speeds(), {
            label: "Transition Speeds",
            icon: "fa-bolt",
            help: "Transition speed"
        });
    };

    SlideshowToolBar.prototype._pseudo_actions.add_slideshow_view_distances = function () {
        return this._make_selector("viewDistance", this.list_view_distances(), {
            label: "View Distance",
            icon: "fa-ellipsis-h",
            help: "Number of slides away from the current that are visible"
        });
    };

    SlideshowToolBar.prototype.visible = function (show) {
        this.element[show ? "slideDown" : "slideUp"](
            100,
            function(){
                events.trigger('resize-header.Page');
            }
        );
    };

    var select_type = CellToolbar.utils.select_ui_generator([
            ["-"            ,"-"            ],
            ["Slide"        ,"slide"        ],
            ["Sub-Slide"    ,"subslide"     ],
            ["Fragment"     ,"fragment"     ],
            ["Skip"         ,"skip"         ],
            ["Notes"        ,"notes"        ],
            ],
            // setter
            function(cell, value){
                // we check that the slideshow namespace exist and create it if needed
                if (cell.metadata.slideshow === undefined){cell.metadata.slideshow = {};}
                // set the value
                cell.metadata.slideshow.slide_type = value;
                },
            //geter
            function(cell){ var ns = cell.metadata.slideshow;
                // if the slideshow namespace does not exist return `undefined`
                // (will be interpreted as `false` by checkbox) otherwise
                // return the value
                return (ns === undefined)? undefined: ns.slide_type;
                },
            "Slide Type");

    var register = function (notebook) {
        CellToolbar.register_callback('slideshow.select',select_type);
        slideshow_preset.push('slideshow.select');

        CellToolbar.register_preset(preset_name, slideshow_preset, notebook);

        // this gets called so early that only events reliably exist...
        // initialize the first time someone fiddles with the cell toolbar
        events.on("preset_activated.CellToolbar", SlideshowToolBar._bootstrap);


        console.log('Slideshow extension for metadata editing loaded.');
    };
    return {'register': register};
});
