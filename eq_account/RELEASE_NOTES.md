## Modul eq_account

#### 19.12.2017
#### Version 1.0.37
##### FIX
- Mini Fix: RechnungsReport: Wenn mehrere Steuersätze verwendet werden.

#### 19.12.2017
#### Version 1.0.36
##### CHG
- Rechnungs-Report: Übersetzungen angepasst; Artikelnr. Zeile (Spalte) Hinzugefügt; Währungszeichen für "Einzelpreis" hinzugefügt

#### 15.12.2017
#### Version 1.0.35
##### ADD
- Rechnungszeilen um das Liefer + Leistungsdatum ergänzt, für Artikel die versendet werden können

#### 24.11.2017
#### Version 1.0.34
##### CHG
Anpassung IDs + Layout.

#### 23.11.2017
#### Version 1.0.33
##### CHG
Vorlage Rechnung - Footer angepasst (grauer HG - neu)

#### 22.11.2017
#### Version 1.0.32
##### CHG
- RechnungsReport: Zahlungskonditionen werden nun aus dem Text der Zahlungskondition gezogen, statt vorher aus dem Namen

#### 22.11.2017
#### Version 1.0.31
##### CHG
- Invoice Vorlage Default Template wird jetzt gezogen

#### 22.11.2017
#### Version 1.0.30
##### CHG
- Invoice Vorlage mit Footer versehen (einkommentiert)

#### 22.11.2017
#### Version 1.0.29
##### CHG
- Custom Layout entfernt.

#### 22.11.2017
#### Version 1.0.28
##### CHG
- Anpassung Mail ID

#### 22.11.2017
#### Version 1.0.27
##### CHG
- Wichtig: Rechnungsvorlage vor dem Update löschen. Dadurch wird das alte Template gelöscht und die Übersetzungen neu erstellt.
- 'Übersetzung laden' überspielt nicht mehr die vorhandene Übersetzung.

#### 21.11.2017
#### Version 1.0.26
##### CHG
- invoice_send_by_email.xml bearbeitet (nbsp entfernt)

#### 21.11.2017
#### Version 1.0.25
##### CHG
- Löschfunktion mail.templates zu 'account' hinzugefügt.

#### 16.11.2017
#### Version 1.0.24
##### CHG
- Modul umbenannt in Finanzen (vorher: Account)

#### 07.11.2017
#### Version 1.0.23
##### CHG
- Description angepasst

#### 06.11.2017
#### Version 1.0.22
##### CHG
- Es wird nur das eingefügte Template zuvor entfernt.

#### 06.11.2017
#### Version 1.0.21
##### ADD
- Mail Template hinzugefügt 'Rechnung'.


#### 11.10.2017
#### Version 1.0.20
##### ADD
- Jira-Issue OE10-10: In den Rechnungsreport ein p-Element mit einer Abfrage auf die payment_term_id hinzugefügt, welcher für die fehlerfreie Installation von dem OCA-Modul
account_payment_partner notwendig ist.

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