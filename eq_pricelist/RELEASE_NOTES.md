## Modul eq_pricelist


#### 16.11.2017
#### Version 1.0.5
##### CHG
- Umbenennen des Moduls zu Preislisten Optimierungen

#### 04.09.2017
#### Version 1.0.4
##### FIX
- Jira Issue OE10-7: Im Zuge der Entfernung des Menüeintrags in VEP-133 war das Datenmodell 'eq_pricelist_item_search' noch in der Datenbank vorhanden
=>
- Delete From ir_model_constraint where name = 'eq_pricelist_item_search_eq_items_id_fkey';
- Delete From ir_model where model = 'eq_pricelist_item_search';
Außerdem musste die Rechtedefinition für dieses Datenmodell noch aus der ir.model.access entfernt werden.

#### 17.08.2017
#### Version 1.0.3
##### CHG
- Menueintrag Positionssuche entfernt (VEP-133)


#### 31.07.2017
#### Version 1.0.2
##### CHG
- Modulbeschreibung erweitert


#### 16.06.2017
#### Version 1.0.1
##### CHG
- Anpassungen für Ordnerstruktur


#### 16.06.2017
#### Version 1.0.0
##### ADD
- Neues Modul für die Anpassungen der Preislisten
- Preislistensuche

