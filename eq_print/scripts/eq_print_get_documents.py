#!/usr/bin/python
# -*- coding: UTF-8 -*-
##############################################################################
# Dieses Skript gehört zum Modul eq_instances
# https://equitania.atlassian.net/wiki/x/XQ9aAw
# Es dient zum Transfer der CSV vom Server zum Druckclient
# Version 1.0.10
# Date 01.02.2017
##############################################################################
#
#    Python Script for Odoo, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import odoorpc
import time
import base64
import os.path
import sys
import os

if sys.platform.startswith('win'):
    try:
        import win32api
        import win32print
    except:
        pass


import logging
_logger = logging.getLogger(__name__)

class odoo_rpc_connector:
    """
    TODO: Connection settings
    """
    # Unter http
    odoo_address = 'localhost'
    odoo_port = 8069
    user = 'admin'
    db = 'v10_ledoptix_test_2'
    pw = 'odoo'
    protocol = 'jsonrpc'

    # Unter https
    # odoo_address = 'test.myodoo.de' ohne Präfix http/https etc.
    # odoo_address = ''
    # odoo_port = 443
    # # Benutzername in Odoo
    # user = 'admin'
    # # Datenbankname in Odoo
    # db = ''
    # # Passwort des Benutzers
    # pw = ''
    # # Protokoll für ht
    # protocol = 'jsonrpc+ssl'

    def odoo_connect(self):
        """
        Prepare the connection to the server
        :return:
        """

        if self.odoo_address.startswith('https'):
            ssl = True
            self.odoo_address = self.odoo_address.replace('https:', '')
            protocol = 'jsonrpc+ssl'
            if self.odoo_port <= 0:
                self.odoo_port = 443
        elif self.odoo_address.startswith('http:'):
            self.odoo_address = self.odoo_address.replace('http:', '')

        while self.odoo_address and self.odoo_address.startswith('/'):
            self.odoo_address = self.odoo_address[1:]

        while self.odoo_address and self.odoo_address.endswith('/'):
            self.odoo_address = self.odoo_address[:-1]

        while self.odoo_address and self.odoo_address.endswith('\\'):
            self.odoo_address = self.odoo_address[:-1]

        odoo_con = odoorpc.ODOO(self.odoo_address, port=self.odoo_port, protocol=self.protocol)
        odoo_con.login(self.db, self.user, self.pw)

        odoo_con.config['auto_commit'] = True  # No need for manual commits
        odoo_con.env.context['active_test'] = False  # Show inactive articles
        return odoo_con


class eq_print_document_processor:

    def __init__(self, interval=10, document_path='/home/ownerp/Documents'):
        self.use_log = False
        self._default_sleep_time = interval
        self._document_path = document_path
        self.module_info = 'eq_print'

        self.connector = odoo_rpc_connector()
        self.odoo = self.connector.odoo_connect()
        self.odoo_spooltable = self.odoo.env['eq.spooltable']
        self.odoo_config_paramas = self.odoo.env['ir.config_parameter']
        self.odoo_logging = self.odoo.env['ir.logging']

    def get_settings(self):
        """
        Get the settings
        :param instance_id:
        :return:
        """
        path = self._document_path # '/home/ownerp/Documents/Test'
        file_format_option = 'pdf'
        interval = self._default_sleep_time
        # if instance_id > 0:
        #     instance = EXPORT_DATA_ENTITY.browse(instance_id)
        #     if instance and instance.eq_export_data_active:
        #         interval = instance.eq_export_data_intervall
        #         if interval < 1:
        #             interval = 1
        #         path = instance.eq_root_directory
        #         file_format_option = instance.eq_file_format
        return interval, path, file_format_option


    def check_for_files(self, path, file_format_option='csv'):
        """
        Checks for new files to be copied to the given directory
        :param path: root directory
        :return:
        """

        new_records = self.odoo_spooltable.get_spooltable_for_user()
        if new_records:

            rec_ids = []
            for rec in new_records:
                if 'id' in rec:
                    rec_ids.append(rec['id'])

            new_files = self.odoo_spooltable.browse(rec_ids)
            for cur_file in new_files:
                try:
                    file_data = cur_file.eq_file

                    file_name = cur_file.eq_document_name  # TODO
                    printer_name = ''
                    if cur_file.eq_printer_id:
                        printer_name = cur_file.eq_printer_id.eq_name
                    if not file_name.endswith('.pdf'):
                        file_name += '.pdf'
                    file_target = ""
                    update_data = {
                        'eq_data_state': 'done',
                    }

                    file_name = "".join([x if x.isalnum() or x in [' ', '-', '+', '.'] else "_" for x in file_name])
                    file_data_dec = base64.b64decode(file_data)
                    file_target = os.path.join(path, file_name)
                    print ("Writing " + file_target)
                    with open(file_target, "wb") as myfile:
                        myfile.write(file_data_dec)

                    if sys.platform.startswith('win'):
                        if not printer_name:
                            printer_name = win32print.GetDefaultPrinter()

                        win32api.ShellExecute(
                            0,
                            "printto",
                            file_target,
                            '"%s"' % printer_name,
                            ".",
                            0
                        )

                    cur_file.do_done()
                except Exception as ex:
                    # print ex

                    self.create_log("Error while copying file", 'check_for_files', self.module_info,
                                           "EXCEPTION", "Error '" + str(ex) + "' while copying file to " + file_target, self.use_log)
    def _get_param_value_as_bool(self, param_name):
        """
        Hilfsmethode für Auslesen von Parameterwerten aus der Tabelle ir.config_parameter mit Umwandlung in einen boolean
        :param param_name:
        :return:
        """
        result = self.odoo_config_paramas.get_param(param_name)
        if not result:
            return False
        return result in ['True', 'true']

    def create_log(self, name, func, path, level, message, create_log_entry = False):
        """
            Erstellt Logeintrag direkt im Odoo
            @cr: Kursor
            @message: Logeintrag mit allen Daten
        """
        if not create_log_entry:
            return

        logger_vals = {
            'name': name,
            'func': func,
            'path': path,
            'line': "/",
            'type': 'server',
            'level': level,
            'message': message
        }
        self.odoo_logging.create(logger_vals)

    def file_process(self):
        """
        :return:
        """

        self.use_log = self._get_param_value_as_bool("eq.print.activate_log")
        self.create_log("file_copy_process - START", 'file_copy_process', self.module_info,
                                         "INFO", "deli file_copy_process wurde gestartet", self.use_log)

        old_settings = '0_'
        while True:
            interval, path, file_format_option = self.get_settings()

            if interval > 0 and path:
                self.check_for_files(path, file_format_option)
            print('Interval: ', interval,'', 'path: ', path)
            # _logger.info('Interval: ' + str(interval) + '; path: ' + path)
            time.sleep(interval)


# proc = eq_print_document_processor(interval=5, document_path='')
# proc.file_process()
