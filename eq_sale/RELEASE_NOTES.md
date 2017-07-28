## Modul eq_sale


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

Benötigte Updatestatements nach Modeländerungen:
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

