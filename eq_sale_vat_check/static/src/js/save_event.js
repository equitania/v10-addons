odoo.define('eq_sale_vat_check.eq_form', function (require) {
    var FormView = require('web.FormView');
    var Model = require('web.Model');
    FormView.include({
        load_record: function () {
                this.$buttons.find('.o_form_button_save').click(function () {
                    console.log($(this).parent());
                    var partner=$(this).parent().find('#o_field_input_8').val();
                    alert(partner);
                });
                this._super.apply(this, arguments);
        }
    });
});