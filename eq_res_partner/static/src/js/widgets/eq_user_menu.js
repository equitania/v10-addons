odoo.define('eq_res_partner.EqUserMenu', function (require) {
"use strict";

var UserMenu = require('web.UserMenu')
var Model = require('web.Model');
var session = require('web.session');

// Overrided base function in UserMenu, for showing the full name in topbar_name

new Model('res.users').query(['display_name']).filter([['id', '=', session.uid]]).first().then(function(res) {
        UserMenu.include({
            do_update: function () {
                var $avatar = this.$('.oe_topbar_avatar');
                if (!session.uid) {
                    $avatar.attr('src', $avatar.data('default-src'));
                    return $.when();
                }
                var self = this

                var topbar_name = res.display_name;
                if(session.debug) {
                    topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
                }
                self.$('.oe_topbar_name').text(topbar_name);
     
     
                var avatar_src = session.url('/web/image', {model:'res.users', field: 'image_small', id: session.uid});
                $avatar.attr('src', avatar_src);
            },
        });
    });
});