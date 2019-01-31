## Modul eq_sale_stock

#### 31.01.2019
#### Version 1.0.16
##### ADD
- Add new field - eq_description in stock.pack.operation
- Extension in _prepare_pack_ops, the value of eq_description is the name of the corresponding move

#### 15.01.2019
#### Version 1.0.15
##### CHG
- move eq_sale_order_id to head form after origin.

#### 20.12.2018
#### Version 1.0.14
##### FIX
- eq_sale_order_id is now set by a compute function not with origin from stock_picking.

#### 28.03.2017
#### Version 1.0.13
##### FIX
- sale.order.line list now reachable

#### 06.03.2017
#### Version 1.0.12
##### CHG
- Kundennummer/Lieferantennumer Anzeige entfernt.

#### 16.11.2017
#### Version 1.0.11
##### CHG
- Umbenennung des Moduls von Sale Stock zu Verkauf & Lager

#### 02.08.2017
#### Version 1.0.10
##### CHG
- Übersetzung angepasst

#### 01.08.2017
#### Version 1.0.9
##### CHG
- Kopf- und Fußtext für stock_picking in eq_stock verschoben


#### 01.08.2017
#### Version 1.0.8
##### CHG
- Zeichnungsnr für die Auftragspositionen und dependency auf eq_mrp entfernt


#### 31.07.2017
#### Version 1.0.7
##### CHG
- Dependency auf eq_mrp wegen eq_drawing_number


#### 28.07.2017
#### Version 1.0.6
##### CHG
- Wikilink in Beschreibung eingefügt

#### 22.06.2017
#### Version 1.0.5
##### CHG
- Übernahme von Kopf- und Fußtexten aus Auftrag

#### 22.06.2017
#### Version 1.0.4
##### CHG
- Kopf- und Fußtext für stock_picking

#### 22.06.2017
#### Version 1.0.3
##### CHG
- Einbau des Feldes eq_drawing_number für die Auftragspositionen


#### 22.06.2017
#### Version 1.0.2
##### CHG
- Anpassungen für VEP-64: Neues Feld eq_sale_order_id für stock_picking


#### 21.06.2017
#### Version 1.0.1
##### CHG
- eq_delivery_date ins Modul eq_sale verschoben


#### 20.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul eq_sale_stock
- Ansicht Auftragspositionen
