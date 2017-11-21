## Modul eq_product

#### 21.11.2017
#### Version 1.0.21
##### CHG
- Logik für Produktnummererzeugung in Datenmodell 'product.product' verschoben (vorher 'product.template').

#### 20.11.2017
#### Version 1.0.20
##### CHG
- Nummergenerator 'eq_product_no' wird automatisch erzeugt (über XML Datei).

#### 17.11.2017
#### Version 1.0.19
##### CHG
- Änderung der Logik für Generierung der Produktnummer

#### 16.11.2017
#### Version 1.0.18
##### CHG
- Umbenennen des Moduls von Produkt zu Produkt Optimierungen

#### 07.11.2017
#### Version 1.0.17
##### FIX
- Übersetzung Produktnummer angepasst.

#### 06.11.2017
#### Version 1.0.16
##### FIX
- Artikelnummer in Produktnummer umbenannt.

#### 06.11.2017
#### Version 1.0.15
##### FIX
- Feld 'default_code' wurde bei dem Modell product.product zusätzlich eingefügt, wodurch eine Diskrepanz entstanden ist.
- Tree View Product Template Interne Referenz in 'Artieklnr.' umbenannt.

#### 31.08.2017
#### Version 1.0.13
##### ADD
- Jira-Issue OEMRP-46:Das Feld 'default_code' ist jetzt ein Constraint. Bei der Produktanlage müssen die Artieklnummer einzigartig sein.
- Wichtig: Constraintdefinition erfolgt nur, wenn es bisher keine Produkte in der Datenbank gibt, welche gegen diese Constraint verstoßen.

#### 09.08.2017
#### Version 1.0.12
##### FIX
- Feld 'default_code' wurde zusätzlich nochmal eingefügt, wodurch eine Diskrepanz entstanden ist.

#### 02.08.2017
#### Version 1.0.11
##### CHG
- Übersetzung angepasst

#### 31.07.2017
#### Version 1.0.10
##### CHG
<b>Error "eq_drawing_numer"</b> <br/>
DB-Update für entfernte View:
DELETE FROM ir_ui_view WHERE name = 'eq.product.template.product.search';

#### 31.07.2017
#### Version 1.0.9
##### CHG
- eq_drawing_number aus eq_product entfernt (neu in eq_mrp)

#### 31.07.2017
#### Version 1.0.8
##### CHG
- Modulbeschreibung erweitert


#### 26.07.2017
#### Version 1.0.7
##### ADD
- Eigene Darstellung für die Produktetiketten erstellt, welche den Standard überschreiben 


#### 24.07.2017
#### Version 1.0.6
##### CHG
- Anzeige der Produktbeschreibung


#### 14.07.2017
#### Version 1.0.5
##### CHG
- VEP-113: Nummerngenerator für Produkte


#### 28.06.2017
#### Version 1.0.4
##### ADD
- Feld für Artikelnummer in die Produkt-Ansicht eingefügt


#### 22.06.2017
#### Version 1.0.3
##### CHG
- VEP-79: Neues Feld eq_drawing_number


#### 20.06.2017
#### Version 1.0.2
##### CHG
- Anpassungen für Ordnerstruktur


#### 16.06.2017
#### Version 1.0.1
##### CHG
- Rechte für Preishistorie hinzugefügt


#### 14.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul für die Erweiterung der Produkte
- Historie für Produktpreise

