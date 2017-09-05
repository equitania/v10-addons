## Modul eq_account

#### 05.09.2017
#### Version 1.0.19
##### FIX
- Feld 'eq_move_ids' hinzugefügt, welche bei Teillieferungen benötigt werden.

#### 05.09.2017
#### Version 1.0.18
##### FIX
- Im Bezug auf Jira Issue VEP-139 gab es den gleichen Fehler, allerdings bei einer Teillieferung. Dieser wurde durch eine angepasste Abfrage behoben.

#### 31.08.2017
#### Version 1.0.17
##### ADD
- Referenzbeleg und Referenznr. werden nun auf den Rechnungen angedruckt

#### 28.08.2017
#### Version 1.0.16
##### FIX
- Auftragszeilen werden nun auch gedruckt wenn die Option für die Kategorien(Sektionen) nicht aktiviert wurde

#### 17.08.2017
#### Version 1.0.15
##### ADD
- Sektionen für die Rechnungen sind nun eingebunden und funktionieren
- Visuelle Anpassungen an dem Summenblock

#### 09.08.2017
#### Version 1.0.14
##### ADD
Rechnungsreport: Lieferdatum / Leistungstag auf Auftragszeilenposition nun im Rechnungsreport enthalten


#### 09.08.2017
#### Version 1.0.13
##### FIX
- BugFix Jira-Issue [VEP-139]: eq_move_id wird nicht mehr bei einer Rückerstattung gesetzt, dies hat den Odoo Error verursacht.

#### 04.08.2017
#### Version 1.0.12
##### ADD/CHG
- Dependency zu eq_sale_stock hinzugefügt (anhand der eq_sale_order_id wird die eq_ref_number (client_order_ref) bis in die stock.picking durchgezogen.
- eq_move_id hinzugefügt: Verbindung zwischen account.invoice.line und dem dazugehörigen stock.move

#### 03.08.2017
#### Version 1.0.11
##### ADD
- Report: USt.ID-Nr. wird nun auf der Rechnung angezeigt, wenn die Rechnung die Steuerzuordnung für EU Kunde mit eingetragener USt.ID-Nr. hat 

#### 01.08.2017
#### Version 1.0.10
##### IMP
- Report erweitert:
- Kopf und Fußtext hinzugefügt. 
- Lieferanschrift umgebaut mit eq_house_no, Citypart usw

#### 01.08.2017
#### Version 1.0.9
##### FIX
- Report: Es wurde noch ein Templating (in rot) angezeigt welche die Kategorien der Auftragszeilen enthalten sollte, dies funktioniert aber noch nicht und wurde nun erstmal wiedr ausgeblendet, damit der Rechnungs-Report wieder fehlerfrei aussieht.

#### 28.07.2017
#### Version 1.0.8
##### CHG
- Modulbeschreibung erweitert

#### 28.07.2017
#### Version 1.0.7
##### CHG
- Konfigurierbarer Seitenumbruch für Kopf- und Fußtexte im Report


#### 28.07.2017
#### Version 1.0.6
##### CHG
- Hilfsfunktionen für Report


#### 03.07.2017
#### Version 1.0.5
##### IMP
Summentabelle der Reports angepasst
- Übersetzung gepflegt
- Position und Ausrichtung korrigiert
- Zusätzliche Steuerzeilen-Tabelle ausgeblendet

#### 30.06.2017
#### Version 1.0.4
##### IMP
- Rechnugnsreport: Übersetzungen angepasst & korrigiert, Pos-Nr. hinzugefügt. Zeilenvariante überarbeitet & andere ausgeblendet

#### 29.06.2017
#### Version 1.0.3
##### CHG
- Rechnungsreport: Neuer Report überschreibt den Standard-Report

#### 22.06.2017
#### Version 1.0.2
##### CHG
- Anzeige von Kopf- und Fußtext bearbeitet


#### 22.06.2017
#### Version 1.0.1
##### CHG
- Neues Feld für Kopftext


#### 19.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul für die Erweiterung des Moduls account
- Erweiterungen für Adressfelder einer Rechnung