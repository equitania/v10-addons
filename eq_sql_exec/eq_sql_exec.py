# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

#from openerp.osv import fields, osv
from openerp import fields,models,api
import string
import random

class eq_sql_exec(models.Model):
    _name = "eq_sql_exec"
    _forbidden_words = ['DROP', 'DELETE']

    @api.model
    def _generate_password(self,size=12, chars=string.ascii_uppercase + string.digits):
        config_parameters = self.env["ir.config_parameter"]
        password = ''.join(random.choice(chars) for _ in range(size))
        config_parameters.set_param("eq_sql_exec_password", password or '', )

        return password



    @api.model
    def test_run(self):
        """
            Simple testrunner just to be able to test our functionality
            
            @cr: cursor
            @uid: user id
        """
        pass

    @api.model
    def execute_sql(self,password, statement):
        """
            Executes sql statement and returns True if excecution was ok
            
            @cr: cursor
            @uid: user id
            @password: password
            @statement: sql statement to be executed against odoo db
            @return: True = execution was OK
        """
        config_parameters = self.env["ir.config_parameter"]
        password_param = config_parameters.get_param("eq_sql_exec_password")
        # first of all, check for admin
        if self._uid != 1:
            print "Wrong user, please use admin!"
            return False

        # no check for password
        if password !=  password_param:
            print "Wrong password for execute_sql provided!"
            return False

        # now check for forbidden words
        # statement = statement.upper()
        test_statement = statement.upper()
        for word in self._forbidden_words:
            index_check = test_statement.find(word)
            if index_check > -1:
                print "Sql statement contains forbidden word!"
                return False

        try:
            self._cr.execute(statement)
            return True
        except:
            return False

    @api.model
    def execute_sql_set_custom_translation(self, password, statement):
        """
            Executes sql statement and returns True if excecution was ok

            @cr: cursor
            @uid: user id
            @password: password
            @statement: sql statement to be executed against odoo db
            @return: True = execution was OK
        """
        config_parameters = self.env["ir.config_parameter"]
        password_param = config_parameters.get_param("eq_sql_exec_password")
        # first of all, check for admin
        if self._uid != 1:
            print "Wrong user, please use admin!"
            return False

        # no check for password
        if password != password_param:
            print "Wrong password for execute_sql provided!"
            return False

        # now check for forbidden words
        # statement = "Select id From ir_translation where name = 'ir.actions.client,help'"
        for word in self._forbidden_words:
            index_check = statement.find(word);
            if index_check > -1:
                print "Sql statement contains forbidden word!"
                return False

        self._cr.execute(statement)
        result = self._cr.fetchall()
        return result
