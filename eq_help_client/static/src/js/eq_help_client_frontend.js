/* Our implementation of help client in frontend*/
odoo.define('eq_help_client_frontend.website', function (require) {
    "use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');

    $("#btnHelp").on("click",function () {
        var software = "Odoo";
        var model = "shop";
        if (result.length > 3){
            model = result[3];
        }
        var view_type = "frontend_page";                                        // constant
        var view_title = $(document).find("title").text();                      // page title
        var view_name = $("meta[property='og:site_name']").attr("content");     // sitename
        var base_url = window.location.href                                     // source url of an actual request

        // get settings from Odoo and open new window with help page
        ajax.jsonRpc("/get_server_infos_json", 'call', {}).then(function (result) {
            window.open(result.help_server_path + '/help/get/' +
                '?software=' + software +
                '&software_version=' + result.software_version +
                '&model=' + model +
                '&view_type=' + view_type +
                '&view_title=' + view_title +
                '&view_name=' + view_name +
                '&base_url=' + base_url,
                '_blank');
        });
    });
});
