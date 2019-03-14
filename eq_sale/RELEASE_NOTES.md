## Modul eq_sale

#### 14.03.2019
#### Version 1.0.96
##### IMP
- SaleReport: Little Padding improvement
- SaleReport: PageBreak fix for Invoice & Shipping-address
 
#### 13.03.2019
#### Version 1.0.95
##### CHG
- Switch to WKHTMLtoPDF 0.12.5 ... Reports and Reportstyles!

#### 05.03.2019
#### Version 1.0.94
##### IMP
- German translation for state done in sale orders

#### 20.02.2019
#### Version 1.0.93
##### CHG
- Report: Changing a wrong Container of Sale-Order Total Container on Reports for future upgrades to WKHTML

#### 09.01.2019
#### Version 1.0.92
##### IMP
- Reports: Changing product quantity and price fields to use the decimal accuracy settings from odoo

#### 04.12.2018
#### Version 1.0.91
##### IMP
- Fixing german translation for "Angebotssdatum"
- Sale Report: Remove Bottom margin for footertext 

#### 16.10.2018
#### Version 1.0.90
##### IMP
- Ticket 6268: Reports: Setting Title and Firstname only when the contact is NOT a company

#### 16.08.2018
#### Version 1.0.89
##### CHG
- Included new css class for optional text-colors in sale orders

#### 10.07.2018
#### Version 1.0.88
##### FIX
- fix sale report language, change o in doc

#### 09.07.2018
#### Version 1.0.87
##### FIX
- (Ticket 5943) Changing Sale Report Address-IF-statements for, if parent address is a company, then show parent company name (instead of "if parent-contact has a name")

#### 21.06.2018
#### Version 1.0.86
##### ADD
- date_order translation with 'Erstelldatum'.
- incoterms translation in 'Incoterms'.

#### 21.06.2018
#### Version 1.0.85
##### ADD
- add website_quote translation for require_payment in a sale order.

#### 21.06.2018
#### Version 1.0.84
##### CHG
- change id in translation for 'benannter Ort'

#### 19.06.2018
#### Version 1.0.83
##### FIX
- Fixing bug with wrong Sequence-No. when using optional products in Sales Order

#### 18.06.2018
#### Version 1.0.82
##### IMP
- Improve IF Statements for Correct customer No

#### 16.06.2018
#### Version 1.0.81
##### FIX
- Correct customer no functionality on sale order Report

#### 11.06.2018
#### Version 1.0.80
##### CHG
- delete sequence from sale.order.lines tree view because now oca module sale_order_line_sequence
- add dependency to sale_order_line_sequence

#### 18.04.2018
#### Version 1.0.79
##### ADD
- add sequence to sale.order.lines tree view in a sale.order.

#### 06.04.2018
#### Version 1.0.78
##### CHG
- delete action for sending sale_order (now in eq_mail_templates)

#### 06.04.2018
#### Version 1.0.77
##### ADD
- move templates into new module eq_mail_templates

#### 29.03.2018
#### Version 1.0.76
##### ADD
- add delivered at place in sale report, if 'DAP' is set as incoterm.

#### 29.03.2018
#### Version 1.0.75
##### CHG
- Changing the template.
- Setting the template to be updated after upgrade of the module.
- Deleting the template and creating again for changes to be shown.

#### 15.03.2018
#### Version 1.0.74
##### ADD
- Nettobetrag bei der Tree-View der Verkaufsaufträge hinzugefügt.

#### 08.03.2018
#### Version 1.0.73
##### CHG
- Domain zum Verkäufer im Verkaufsauftrag angepasst, sodass nur 'Interne Nutzer' hierbei aufgelistet werden.

#### 06.03.2018
#### Version 1.0.72
##### IMP
- Kundennummer/Lieferantennumer Anzeige entfernt.

#### 09.02.2018
#### Version 1.0.71
##### IMP
- (#5313 - VEP-177) Verkaufsreport: Kontakt E-Mailadresse hat nun mehr Platz und bricht bei zu langen Adressen nun um, statt den Block zu verziehen.

#### 01.02.2018
#### Version 1.0.70
##### ADD
- Felder Fußtext (sale.order) und Beschreibung (sale.order.line) jetzt mit translate = True definiert.

#### 30.01.2018
#### Version 1.0.69
##### FIX
- Ticket 5101: Steuer bei prozentualer/fixer Rechnungserzeugung wurde nicht korrekt gesetzt.

#### 25.01.2018
#### Version 1.0.68
##### FIX
- BugFix: Sobald der type einers res.partner = False, war es nicht mehr möglich ein Angebot anzulegen. Abfrage hinzugefügt.

#### 24.01.2018
#### Version 1.0.67
##### ADD
- Nettopreis im Angebot hinzugefügt

#### 24.01.2018
#### Version 1.0.66
##### CHG
- Preview-Button Einstellungen werden jetzt nur noch bei der Erstellung eines neuen Angebots gezogen (Verhindert jetzt die langen Ladezeiten in den Verkaufeinstellungen)

#### 23.01.2018
#### Version 1.0.65
##### FIX
- Preview-Button vom Typ 'object' defniert. Dadurch ist dieser wieder ausführbar.

#### 09.01.2018
#### Version 1.0.64
##### ADD
- Fehlende Reportlogik in sale.order hinzugefügt (Anzeige Lieferdatum und Anzeige Lieferdatum als KW). Konfigurationscheckboxen waren bereits vorhanden.

#### 19.12.2017
#### Version 1.0.63
##### CHG
- Report: Übersetzungen angepasst

#### 27.11.2017
#### Version 1.0.62
##### CHG
- Neue ID Vergabe
- Anrede berücksichtigt

#### 23.11.2017
#### Version 1.0.61
##### CHG
Vorlage Sales order - Footer angepasst (grauer HG - neu)

#### 22.11.2017
#### Version 1.0.60
##### CHG
- Sale Order Vorlage Default Template wird jetzt gezogen

#### 22.11.2017
#### Version 1.0.59
##### CHG
- Sale_Order Vorlage mit Footer versehen (einkommentiert)

#### 22.11.2017
#### Version 1.0.58
##### CHG
- Custom Layout entfernt.

#### 22.11.2017
#### Version 1.0.57
##### CHG
- Anpassung Mail ID + Identifikator.

#### 21.11.2017
#### Version 1.0.56
##### CHG
- Textänderung in Beschreibung der Params. Kein [equitania] Text mehr

#### 20.11.2017
#### Version 1.0.55
##### CHG
- inherit_id entfernt, welche die Warning 'ir.actions.act_window.write() with unknown fields: inherit_id' verursachte.

#### 07.11.2017
#### Version 1.0.54
##### ADD
- Description angepasst.

#### 06.11.2017
#### Version 1.0.53
##### CHG
- Es wird nur das eingefügte Template zuvor entfernt.

#### 06.11.2017
#### Version 1.0.52
##### ADD
- Mail Template 'Sale order' hinzugefügt.

#### 19.10.2017
#### Version 1.0.51
##### CHG
- Logger deaktiviert. Ab jetzt zeigen wir die Debuginfos in der Konsole nicht mehr an

#### 17.10.2017
#### Version 1.0.50
##### FIX
- Dependency zu 'website_quote' hinzugefügt.

#### 11.10.2017
#### Version 1.0.49
##### FIX
- Da das Beschreibungsfeld in der Sale.Order.Line ein required Feld ist wird hier ein Leerzeichen gesetzt, sobald das ausgewählte Produkt keine Produktbeschreibung besitzt.

#### 09.10.2017
#### Version 1.0.48
##### ADD
- Preview Button im Angebot jetzt über Flag in den Einstellungen (Verkauf) steuerbar ob er ein- oder ausgeblendet wird.

#### 06.10.2017
#### Version 1.0.47
##### CHG
- Kundenreferenz im Tab 'Weitere Information' entfernt und in der Hauptmaske zum Verkaufauftrag/Angebot hinzugefügt.

#### 18.09.2017
#### Version 1.0.46
##### CHG
- Kundennumer in List-View hinzugefügt.

#### 15.09.2017
#### Version 1.0.45
##### CHG
- Kundennumer aus List-View entfernt

#### 14.09.2017
#### Version 1.0.44
##### CHG
- Listview als Defaultansicht
- Neue Felder für Listview

#### 13.09.2017
#### Version 1.0.43
##### CHG
- Zwei Printstatements entfernt, damit die Console wieder sauber ausgegeben wird

#### 12.09.2017
#### Version 1.0.42
##### IMP
- Erweiterung um Funktion _eq_display_address

#### 17.08.2017
#### Version 1.0.41
##### CHG
- Anpassungen für Ansicht Report Layoutkategorien (Anzeige des neuen Feldes Trennlinie)


#### 17.08.2017
#### Version 1.0.40
##### IMP
- Visuelle Anpassungen an dem Summenblock sowie an den Sektionen


#### 10.08.2017
#### Version 1.0.39
##### CHG
- Dependency und Report angepasst für das Modul "delivery" um den Frachtführer hinzuzufügen


#### 10.08.2017
#### Version 1.0.38
##### FIX
- Report: Carrier_ID aus dem Report auskommentiert, da es sonst zu Problemen führen kann wenn die Option für die Versandkosten-hinzufügen nicht aktiviert ist

#### 08.08.2017
#### Version 1.0.37
##### IMP
- Erweiterung der Funktionalität des Reports "Angebot" um neue Logik für optionale Produkte, VEP-138, eq_sale: Optionale Produkte, falsche Zwischensumme

#### 03.08.2017
#### Version 1.0.36
##### ADD
- Report: USt.ID-Nr. wird nun auf dem Angebot angezeigt, wenn das Angebot die Steuerzuordnung für EU Kunde mit eingetragener USt.ID-Nr. hat 


#### 01.08.2017
#### Version 1.0.35
##### IMP
Report verbesserungen
- Kopf und Fußtext hinzugefügt, inkl. Seitenumbruch
- Anordnung und Darstellung der Angebots-Fußdaten verbessert
- Delivery Method in den Report eingefügt
- Unnötige Abstände entfernt
- Paar Übersetzungen angepasst für die neue Darstellung



#### 01.08.2017
#### Version 1.0.34
##### CHG
- Report: Übersetzung für die "Sale Order" ist nichtmehr "Verkaufsauftrag" sondern "Auftragsbestätigung"

#### 28.07.2017
#### Version 1.0.33
##### CHG
- Wikilink in Beschreibung eingefügt

#### 28.07.2017
#### Version 1.0.32
##### CHG
- Konfigurierbarer Seitenumbruch für Kopf- und Fußtexte im Report


#### 28.07.2017
#### Version 1.0.31
##### CHG
- Reportfunktion für Test auf gesetzten Inhalt eines HTML-Textes


#### 26.07.2017
#### Version 1.0.30
##### CHG
- Änderungen der Bezeichner für Dezimalstelleneinstellungen

Updates für alte Bezeichner:
UPDATE decimal_precision SET name = 'Sale Unit of Measure Report [eq_sale]' WHERE name = 'Sale Quantity Report';
UPDATE decimal_precision SET name = 'Sale Price Report [eq_sale]' WHERE name = 'Sale Price Report';
UPDATE decimal_precision SET name = 'Sale Weight Report [eq_sale]' WHERE name = 'Sale Weight Report';hase';


#### 26.07.2017
#### Version 1.0.29
##### CHG
- Erweiterungen für die Dezimalstellen in Reports


#### 25.07.2017
#### Version 1.0.28
##### CHG
- Übersetzung für die neue Steuerzeile durch die optionalen Positionen ergänzt

#### 25.07.2017
#### Version 1.0.26
##### CHG
- Automatisches Setzen des Lieferdatums und "Tage bis Auslieferung" bei Änderung

#### 25.07.2017
#### Version 1.0.26
##### ADD
- Optionale

#### 24.07.2017
#### Version 1.0.25
##### ADD
- Optionale Positionen für Angebote (Nun auch in Reports enthalten)


#### 24.07.2017
#### Version 1.0.24
##### CHG
- Optionale Positionen für Angebote


#### 24.07.2017
#### Version 1.0.23
##### CHG
- Vererbung für Sektionen statt neue Tabelle
Benötigte Updatestatements nach Modeländerungen:<br>
<b>Fehler - Das Feld `sale_layout_cat_id` existiert nicht</b><br>
DELETE from ir_ui_view where name = 'sale.order.form.inherit_1';
DELETE from ir_model where name = 'sale_layout.category';

#### 24.07.2017
#### Version 1.0.22
##### CHG
AngebotsReport angepasst:
- Titel, Vorname, Namenszusatz, Hausnummer und Straße2 in den separaten Liefer & Rechnungsadressen unten im Angebot ergänzt
- Standard Incoterm ausgeblendet/überschrieben
- Lieferbedingungen ergänzt

#### 07.07.2017
#### Version 1.0.21
##### FIX
- VEP-112: Fußtext ist doppelt drin


#### 06.07.2017
#### Version 1.0.20
##### FIX
- VEP-111: Fix für Fehler bei Anlage eines Angebots

#### 05.07.2017
#### Version 1.0.19
##### CHG
- VEP-92: Begonnen mit Sektionen im Angebot


#### 05.07.2017
#### Version 1.0.18
##### CHG
- VEP-17: Kopf- und Fußtext der Rechnungen abhängig von Einstellung "Benutze Kopf- und Fusstext aus Auftrag"


#### 30.06.2017
#### Version 1.0.17
##### CHG
- Übersetzung für die Zwischensumme hinzugefügt

#### 29.06.2017
#### Version 1.0.16
##### IMP
- Verkaufsreport: Verbesserung in Details wie Ländernamen bei Kunden aus einem anderen Land, Pos-Nr und Kategorien für Auftragszeilen


#### 28.06.2017
#### Version 1.0.15
##### CHG
- Neuer Aufbau der Auftragszeilen, mit Sektionen und zuschaltbarer Mengeneinheit

#### 27.06.2017
#### Version 1.0.14
##### FIX
- Korrektur für Wechsel des Kunden in Angebotsmaske


#### 23.06.2017
#### Version 1.0.13
##### CHG
- Report ersetzt nun den Standard Verkaufsauftrag-Report
- Diverse nichtmehr benötigte Klassen wurden bereinigt

#### 23.06.2017
#### Version 1.0.12
##### ADD
- Report: Lieferdatum auf Auftragszeile
- Report: Platzhalter für Zeichnungsnummer
- Report: Platzhalter für Rahmenauftragsnr.

#### 22.06.2017
#### Version 1.0.11
##### CHG
- Anpassung für Rechnungserstellung


#### 22.06.2017
#### Version 1.0.10
##### CHG
- Einbau des Kopftextes, Verweis auf eq_report_pattern entfernt


#### 21.06.2017
#### Version 1.0.9
##### CHG
- VEP-78: Erweiterungen für sale_order_line


#### 21.06.2017
#### Version 1.0.8
##### IMP
- Mehrere Verbesserungen am Report:
Neu: Neue Felder für Kopf- und Fußtext mit HTML Editor werden verwendet
Neu: "Unser Referenzbeleg" im Reportkopf
Neu: "Angebot gültig bis" Feld im Report hinzugefügt
Neu: Die Kundenanschrift enthält nun auch Anrede, Vorname, Hausnr, Stadtteil und eq_name2
Verbessert: Zahlungsbedingungen haben nun ein eigenes Label
Verbessert: Das Auftragsdatum heißt nun ggf. Angebotsdatum, solange es ein Angebot ist.


#### 20.06.2017
#### Version 1.0.7
##### CHG
- Erweiterungen für Kommentare


#### 20.06.2017
#### Version 1.0.6
##### CHG
- VEP-38: Erweiterungen für Verkaufseinstellungen


#### 20.06.2017
#### Version 1.0.5
##### CHG
- Anpassungen für Ordnerstruktur


#### 19.06.2017
#### Version 1.0.4
##### CHG
- Erweiterungen für Adressinformationen für sale_order

#### 19.06.2017
#### Version 1.0.3
##### ADD
- Erste ReportVersion (EQ) Verkaufsreport

#### 19.06.2017
#### Version 1.0.2
##### CHG
- super-Aufruf für Wechsel des Feldes partner_id


#### 16.06.2017
#### Version 1.0.1
##### CHG
- Eigene Tabelle für Lieferbedingungen
- Smartbuttons Angebote und Verkäufe für Kundenansicht
- Ersteller eines Datensatzes wird automatisch als Verkäufer gesetzt

#### 14.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul eq_sale
- Anzeige der offenen und abgeschlossenen Verkäufe

