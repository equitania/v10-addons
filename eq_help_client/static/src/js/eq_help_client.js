odoo.define('eq_help_client.HelpClient', function (require) {
    "use strict";
    var eq_hide_parts = false;
    var eq_show_left_div = false

    var core = require('web.core');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var ViewManager = require('web.ViewManager');
    var ControlPanel = require('web.ControlPanel');
    var session = require('web.session');
    session.help_params = false;

    ControlPanel.include({
        _toggle_visibility: function(visible) {
            if (eq_hide_parts){
                // to be able to use help button really on EACH backend page, just set visibility always to TRUE
                $(".breadcrumb").hide();
                $(".o_cp_searchview").hide();

                if (eq_show_left_div){                  // extra logic for cloud
                    $(".o_list_buttons").show();
                    $(".o_cp_buttons").show();
                }
                else{
                 $(".o_list_buttons").hide();
                 $(".o_cp_buttons").hide();
                }

                $(".o_cp_right").addClass("eq_only_help_client");
                visible = true;
            }
            else{
                $(".breadcrumb").show();
                $(".o_cp_searchview").show();
                $(".o_list_buttons").show();
                $(".o_cp_buttons").show()
                $(".o_cp_right").removeClass("eq_only_help_client");
            }

            this.do_toggle(visible);
            if (!visible && !this.$content) {
                this.$content = this.$el.contents().detach();
            } else if (this.$content) {
                this.$content.appendTo(this.$el);
                this.$content = null;
            }
        },

        start: function(){
            this._super.apply(this, arguments);
            this._toggle_visibility(true);
            this.nodes = _.extend(
                this.nodes,
                {$eq_help_client_buttons: this.$('.o_eq_help_client_buttons')});
            //this._toggle_visibility(false);
        },
    });

    ViewManager.include({
        init: function(parent, dataset, views, flags, options) {
            // are we dealing with config pages
            if (dataset.model.includes('config') || dataset.model.includes('board.board') ||
                dataset.model.includes('eq.cloud.settings')){
                eq_hide_parts = true;   // yes - so hide parts
                eq_show_left_div = false;
                if (dataset.model.includes('eq_cloud_base_config_folders')){
                    eq_show_left_div = true;
                }
            }
            else{
                eq_hide_parts = false;  // no
            }

            var self = this;
            this._super(parent, dataset, views, flags, options);
            if (!session.help_params) {
                session.help_params = {};
                console.log('Help Client load params');
                var P = new Model('ir.config_parameter');
                P.call('get_param', ['help_server_path']).then(function (server_path) {
                    session.help_params.help_server_path = server_path;
                });
                P.call('get_param', ['software_type']).then(function (sw_type) {
                    if (sw_type) {
                        session.help_params.software_type = sw_type;
                    } else {
                        session.help_params.software_type = "Odoo";
                    }
                });
            }
        },

        /**
         * This function render the help button with the informations received
         * from the call to the method build_url from the eq_help_client controller
         */
        render_help_button: function(){
            var self = this;
            var $helpButton = $(QWeb.render("HelpClient.Button", {'view_manager': this,}));
            $helpButton.tooltip();
            $helpButton.on('click', function (event) {
                if (!session.help_params.help_server_path){
                    console.warn("Server Path is not set!");
                    return false;
                }

                // Source_Client = web.base.url
                window.open(session.help_params.help_server_path + '/help/get/' +
                    '?software=' + session.help_params.software_type +
                    '&software_version=' + window.odoo.session_info.server_version_info[0] +
                    '&model=' + self.dataset.model +
                    '&view_type=' + self.active_view.type +
                    '&view_title=' + self.active_view.title +
                    '&view_name=' + self.active_view.fields_view.name +
                    '&base_url=' + session["web.base.url"],
                    '_blank');
            });
            return $helpButton;
        },

        /**
         * This function render the help buttons container on the view.
         * It should be called after start() by render_view_control_elements.
         * @param {control_elements} the list of control elements to display into the ControlPanel
         */
        render_help_buttons: function(control_elements){
            if (! control_elements.$eq_help_client_buttons){
                control_elements.$eq_help_client_buttons = $('<div/>');
            }
            var self = this;
            var $helpButton = self.render_help_button();
            control_elements.$eq_help_client_buttons = $helpButton;
            // update the control panel with the new help button
            self.update_control_panel({cp_content: _.extend({}, self.searchview_elements, control_elements)}, {clear: false});
        },

        render_view_control_elements: function() {
            var control_elements = this._super.apply(this, arguments);
            this.render_help_buttons(control_elements);
            return control_elements;
        },

    });
});
