.. image:: https://rm.ownerp.io/staff/MyOdooLogo.png
   :alt: Power by MyOdoo
   :target: https://www.myodoo.de

MyOdoo Help Client
==================

Erweitert Odoo um eine kontextsensitive Hilfe.
Das Modul sendet entsprechend der Odoo Seite, auf der Sie sich gerade befinden, eine verschlüsselte Anfrage an unseren Index-Server (https://help.myodoo.io).

Dort wird Ihr Aufruf an https://equitania.atlassian.net/wiki/spaces/MH/overview weitergeleitet. 
Wenn es noch keine entsprechende Hilfeseite gibt, landen Sie auf der Startseite.
Wir bemühen uns aber die ensprechenden Suchanfragen zu dokumentieren.

.. image:: https://rm.ownerp.io/flags/de.png
    :width: 75

Installation
============

Um dieses Modul zu installieren, müssen Sie nur das Modul auswählen und sicherstellen, dass Ihre Abhängigkeiten verfügbar sind.

Konfiguration
=============

Es ist nichts zu konfigurieren:
- das Modul legt unter den Systemparametern den Eintrag "help_server_path" an.
- Dort steht der Link auf unseren Index-Server 

Verwendung
==========

Auf unserem Index-Server werden folgende Informationen gespeichert:

- Source Client (Woher kommt die Anfrage - keine IP NUR der Namen des Systems)
- Version des Odoo Systems (10,12 etc.)
- Daten Modell der Anfrage z.B. crm.lead, res.partner etc.
- Ansichtsart z.B. list, form, kanban etc.
- Name der Ansicht z.B. crm.lead.tree.lead
- Datum der Anfrage

Es werden keine personenbezogenen Daten gespeichert.
Die Speicherung findet in Frankfurt am Main/Deutschland statt.
Näheres entnehmen Sie bitte unserer Datenschutz-Erklärung https://www.myodoo.de/datenschutz

Known issues / Roadmap
======================

Contributors
------------

* Martin Schmid <m.schmid@equitania.com>
* Wolfgang Pichler <office@callino.at>

Maintainer
----------

.. image:: https://rm.ownerp.io/staff/EquitaniaLogo.png
   :alt: Equitania Software GmbH
   :target: https://www.equitania.de

* Equitania Software GmbH
* Weiherstrasse 13
* 75173 Pforzheim
* Germany
* https://www.myodoo.de

Copyrights & License
====================

* Copyright 2014 - now by Equitania Software GmbH - Germany - https://www.equitania.de
* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

.. image:: https://rm.ownerp.io/staff/ownERP_Logo.png
   :alt: ownERP - ERP as a Service
   :target: https://www.ownerp.de


.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3