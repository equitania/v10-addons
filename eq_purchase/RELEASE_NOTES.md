## Modul eq_purchase

#### 22.11.2017
#### Version 1.0.28
##### CHG
- Anpassung Mail ID + Identifikator.

#### 21.11.2017
#### Version 1.0.27
##### CHG
- Mailvorlage für Bestellung und RFQ (Angebotsanfrage) bearbeitet (nbsp entfernt; Schlussormel erweitert;)

#### 21.11.2017
#### Version 1.0.26
##### CHG
- Textänderung in Beschreibung der Params. Kein [equitania] Text mehr

#### 16.11.2017
#### Version 1.0.25
##### CHG
- Modul umbenannt zu Einkauf Optimierungen

#### 07.11.2017
#### Version 1.0.24
##### CHG
- Description angepasst.

#### 06.11.2017
#### Version 1.0.23
##### CHG
- Es wird nur das eingefügte Template zuvor entfernt.

#### 06.11.2017
#### Version 1.0.22
##### ADD
- Mail Template 'RFQ und Bestellung' hinzugefügt.

#### 25.10.2017
#### Version 1.0.21
##### FIX
- Ticket 4952: Angebotsanfrage ohne Positionen kann jetzt gelöscht werden.

#### 18.09.2017
#### Version 1.0.20
##### CHG
- Lieferantennumer in List View wieder hinzugefügt.

#### 15.09.2017
#### Version 1.0.19
##### CHG
- Lieferantennumer aus List View entfernt

#### 15.09.2017
#### Version 1.0.18
##### CHG
- Listview als Defaultansicht
- Neue Felder für Listview


#### 01.09.2017
#### Version 1.0.17
##### IMP
- Einkaufs Report: Angleichung der Darstellung vom Summenblock zu den anderen Reports

#### 02.08.2017
#### Version 1.0.16
##### IMP
- Report: Kopf & Fußtext nun korrigiert und Funktion für Seitenumbruch enthalten

#### 31.07.2017
#### Version 1.0.15
##### CHG
- Link zum Wikiartikel geändert

#### 31.07.2017
#### Version 1.0.14
##### CHG
- Equitania Bestellungen in Einkauf umbenannt

#### 31.07.2017
#### Version 1.0.13
##### CHG
- Modulbeschreibung erweitert

#### 28.07.2017
#### Version 1.0.12
##### CHG
- Konfigurierbarer Seitenumbruch für Kopf- und Fußtexte im Report


#### 28.07.2017
#### Version 1.0.11
##### CHG
- Reportfunktion für Test auf gesetzten Inhalt eines HTML-Textes


#### 27.07.2017
#### Version 1.0.10
##### ADD
- Angebots-Report: Neu hinzugefügt. Sowie Verbesserungen in der Bestellung

#### 26.07.2017
#### Version 1.0.9
##### CHG
- Änderungen der Bezeichner für Dezimalstelleneinstellungen

Updates für alte Bezeichner:
UPDATE decimal_precision SET name = 'Purchase Unit of Measure Report [eq_purchase]' WHERE name = 'Purchase Quantity Report';
UPDATE decimal_precision SET name = 'Purchase Price Report [eq_purchase]' WHERE name = 'Purchase Price Report';
UPDATE decimal_precision SET name = 'Purchase Product Price [eq_purchase]' WHERE name = 'Product Price Purchase';
UPDATE decimal_precision SET name = 'Purchase Unit of Measure [eq_purchase]' WHERE name = 'Product Quantity Purchase';

#### 26.07.2017
#### Version 1.0.8
##### CHG
- Formatierung für Menge und Preis pro für die Bestellpositionen über Einstellungen aus decimal_precision.xml


#### 26.07.2017
#### Version 1.0.7
##### CHG
- Erweiterungen für die Dezimalstellen in Reports

#### 26.07.2017
#### Version 1.0.6
##### ADD
- Einkaufs-Report

#### 25.07.2017
#### Version 1.0.5
##### CHG
- Feld user_id für purchase_order


#### 25.07.2017
#### Version 1.0.4
##### CHG
- Anzeige Geplantes Datum für Report


#### 25.07.2017
#### Version 1.0.3
##### CHG
- Korrekturen für Klassennamen (Fehler in Bestellungen)


#### 24.07.2017
#### Version 1.0.2
##### CHG
- Begonnen mit Reporteinstellungen für Einkauf

#### 22.06.2017
#### Version 1.0.1
##### CHG
- Feld für Kopftext hinzugefügt
- Anpassungen für Formview


#### 19.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul für die Erweiterung der Bestellungen
- Übernahme der Fremdnr beim Wechsel des Partners

