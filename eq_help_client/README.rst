MyOdoo Help Client
==================

Erweitert Odoo um eine kontextsensitive Hilfe.
Das Modul sendet entsprechend der Odoo Seite, auf der Sie sich gerade befinden, eine verschlüsselte Anfrage an unseren Index-Server (https://help.myodoo.io).
Dort wird Ihr Aufruf an https://equitania.atlassian.net/wiki/spaces/MH/overview weitergeleitet. 
Wenn es noch keine entsprechende Hilfeseite gibt, landen Sie auf der Startseite.
Wir bemühen uns aber die ensprechenden Suchanfragen zu dokumentieren.

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

Equitania Software GmbH
Weiherstrasse 13
75173 Pforzheim
Germany
https://www.myodoo.de