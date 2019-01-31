## Modul eq_stock

#### 31.01.2019
#### Version 1.0.29
##### FIX
- Fixed missing "float_compared" 

#### 22.01.2019
#### Version 1.0.28
##### FIX
- FIX odoo standard in action_assign from stock_move when an ancestor exists and product type is consu. Then check if the state of ancestor is done, if yes continue with move_assign. 

#### 22.01.2019
#### Version 1.0.28
##### FIX
- FIX odoo standard in action_assign from stock_move when an ancestor exists and product type is consu. Then check if the state of ancestor is done, if yes continue with move_assign. 

#### 05.12.2018
#### Version 1.0.27
##### IMP
- Report: Delivery and Packlist: Parent Company name will not be printed anymore when the address is a company as well.

#### 29.10.2018
#### Version 1.0.26
##### FIX
- Ticket 6321: stockpicking report: changing product_qty to product_uom_qty

#### 16.10.2018
#### Version 1.0.25
##### FIX
- Ticket 6268: Reports: Setting Title and Firstname only when the contact is NOT a company

#### 09.07.2018
#### Version 1.0.24
##### FIX
- (Ticket 5943) Changing Stock & Picking Report Address-IF-statements for, if parent address is a company, then show parent company name (instead of "if parent-contact has a name")

#### 02.07.2018
#### Version 1.0.23
##### CHG
- Ticket 5880: Change translation

#### 20.06.2018
#### Version 1.0.22
##### IMP
- Stock Delivery report: shows only products which have Quantity Done (qty_done) bigger then 0.

#### 18.06.2018
#### Version 1.0.21
##### IMP
- Improve IF Statements for Correct customer No

#### 16.06.2018
#### Version 1.0.20
##### FIX
- Correct customer no functionality on STOCKPICKING Report

#### 08.05.2018
#### Version 1.0.19
##### CHG
- change name field of stock.move from char to text (qmk mail).

#### 08.05.2018
#### Version 1.0.18
##### ADD
- Access rules for the model eq_deactivate_old_records_func

#### 04.05.2018
#### Version 1.0.17
##### ADD
- added new incoterms together with deactivation of old ones

#### 23.04.2018
#### Version 1.0.16
##### CHG
- opportunity to change the description in a stock.picking initial demand.

#### 23.04.2018
#### Version 1.0.15
##### CHG
- Adding some name-classes to some TD/TH Tabelobjects in report, to fix some installproblems of other LOT-Modules

#### 26.03.2018
#### Version 1.0.14
##### ADD/CHG
- stock.picking shows all locations of parent location.

#### 06.03.2018
#### Version 1.0.13
##### ADD
- Kundenreferenz wird jetzt auch im Lieferschein angezeigt.

#### 09.02.2018
#### Version 1.0.12
##### IMP
- (#5313 - VEP-177) Lieferscheinreport: Kontakt E-Mailadresse hat nun mehr Platz und bricht bei zu langen Adressen nun um, statt den Block zu verziehen.

#### 02.02.2018
#### Version 1.0.11
##### IMP
- Lieferschein Enthält nun Logik für Serien & Chargen-Nummern. Packschein enthält nun den Barcode der vorher in den Kopfdaten abgedruckt wird.

#### 18.01.2018
#### Version 1.0.10
##### IMP
- Lieferschein Report: Enthält nichtmehr die Anzeige für Packvorgänge. Zeigt stattdessen nun immer auch den Beschreibungstext welcher zum Produkt im Angebot/Auftrag mit hinterlegt wurde.

#### 19.12.2017
#### Version 1.0.9
##### CHG
- Lieferscheinreport: "Unsere Referenznr." heißt nun "Auftragsnr."

#### 19.12.2017
#### Version 1.0.8
##### CHG
- Lieferschein Report: Übersetzungen gepflegt; Artikel Nr. + Code getrennt zu einzelnen Spalten; Barcode funktioniert nun, aber auskommentiert da vermutlich nicht benötigt.

#### 16.11.2017
#### Version 1.0.7
##### CHG
- Modul umbenannt zu Lager Optimierungen

#### 10.08.2017
#### Version 1.0.6
##### CHG
- Dependency und Report angepasst für das Modul "delivery" um den Frachtführer und Gewicht hinzuzufügen

#### 01.08.2017
#### Version 1.0.5
##### IMP
Report: Kopf und Fußtext hinzugefügt, inkl. Seitenumbruch

#### 01.08.2017
#### Version 1.0.4
##### CHG
- Erweiterungen für stock_picking: Kopf- und Fußtexte

#### 28.07.2017
#### Version 1.0.3
##### ADD
- Wikilink in Beschreibung eingefügt

#### 25.07.2017
#### Version 1.0.2
##### ADD
- Report: Packliste

#### 24.07.2017
#### Version 1.0.1
##### ADD
- Lieferschein Report hinzugefügt

#### 04.07.2017
#### Version 1.0.0
##### ADD
- Initialversion (Template Vorlage)
