## eq_report_pattern 

#### 29.03.2019
#### Version 1.0.37
##### FIX
- German Translation 

#### 28.03.2019
#### Version 1.0.36
##### FIX
- Section is taken from the document template.
- Translation for positions in the template.

#### 19.03.2019
#### Version 1.0.35
##### FIX
- Onchange on document template appends the positions instead of replacing the existing ones.

#### 19.03.2019
#### Version 1.0.34
##### FIX
- Changed order of loading the models, this fixes initial installation errors.

#### 13.03.2019
#### Version 1.0.33
##### ADD
- Added pricelists for document template.

#### 13.03.2019
#### Version 1.0.32
##### FIX
- Fixing Ascii-Error

#### 18.02.2019
#### Version 1.0.31
##### CHG
- Translation change 

#### 18.02.2019
#### Version 1.0.30
##### ADD
- Documents that have no model can be selected everywhere.
- Added models for Invoice and Delivery.
- Added default value that is selected automatically on creation and is unique.

#### 07.02.2019
#### Version 1.0.29
##### ADD
- Added Document template for purchase orders.
- Two types of Document Templates one for Sale Orders and One for Purchase Orders.
- For Purchase Orders Templates the cost price is taken by default.
- Added menu in the purchase app to see Templates. 

#### 16.04.2018
#### Version 1.0.28
##### FIX
- lines changed to eq.sale.quote.line like v8

#### 15.03.2018
#### Version 1.0.27
##### ADD
- Dokumentenvorlage in Verkaufsauftrag hinzugefügt (Tree View)

#### 24.01.2018
#### Version 1.0.26
##### ADD
- Dokumentenvorlage in Angebot hinzugefügt (Tree View)

#### 16.11.2017
#### Version 1.0.25
##### CHG
- Modul zu "Dokumenten Bausteine" umbenannt

#### 09.10.2017
#### Version 1.0.24
##### CHG
- Das Feld 'Zahlungen' (require_payment) wird jetzt unter dem Verkaufsteam im Tab 'Weitere Informationen' eingefügt => Änderung notwendig, da das Modul eq_sale die Kundenreferenz in die Auftragsmaske verschoben hat.

#### 10.08.2017
#### Version 1.0.22
##### FIX
- Korrekturen für Dokumentenvorlage

#### 02.08.2017
#### Version 1.0.21
##### CHG
- Dependencys eq_sale_stock entfernt.

#### 01.08.2017
#### Version 1.0.20
##### CHG
- Tab "Produktvorschläge" wird unter Verkaufsaufträgen nun ausgeblendet

#### 01.08.2017
#### Version 1.0.19
##### CHG
- Feld comment als HTML-Feld für Rechnungen (Workaround da Feld trotz Erweiterung in eq_account als Textfeld angezeigt wurde, falls eq_report_pattern installiert wurde)

#### 31.07.2017
#### Version 1.0.18
##### DEL
- Lieferschein Duplikat (Template) gelöscht

#### 31.07.2017
#### Version 1.0.17
##### CHG
- Dependency zu Fertigung entfernt

#### 31.07.2017
#### Version 1.0.16
##### CHG
- Dependency auf eq_mrp wegen eq_drawing_number


#### 31.07.2017
#### Version 1.0.15
##### CHG
- Ausblenden der Seite Produktvorschläge wieder zurückgenommen (führte zum Ausblenden eines falschen Tabs)


#### 31.07.2017
#### Version 1.0.14
##### CHG
- Modulbeschreibung erweitert

#### 24.07.2017
#### Version 1.0.13
##### CHG
- Partnereinstellungen für Formatierung des Lieferdatum und des geplanten Datums im Report


#### 24.07.2017
#### Version 1.0.12
##### CHG
- Ausblenden der Seite Produktvorschläge


#### 24.07.2017
#### Version 1.0.11
##### CHG
- Div und Label für Feld template_id entfernt (Leerzeile in Anzeige für Lieferadresse)


#### 24.07.2017
#### Version 1.0.10
##### CHG
- Dokumentenvorlage verschoben

#### 22.06.2017
#### Version 1.0.9
##### CHG
- Anpassungen nach Auslagerung der Kopf- und Fußtexte


#### 22.06.2017
#### Version 1.0.8
##### CHG
- Kopft- und Fußtexte verschoben


#### 22.06.2017
#### Version 1.0.7
##### CHG
- Kopftext ins Modul eq_sale verschoben
- für sale_order: note statt eq_footer verwenden


#### 19.06.2017
#### Version 1.0.6
##### [ADD/CHG]
- Header und Footer zu purchase und account_invoice hinzgefügt, note Feld ausgeblendet

#### 13.06.2017
#### Version 1.0.5
##### [FIX/CHG]
- Bug behoben, welcher eine Anlage einer zweiten Vorlage verhinderte (create Methode angepasst)
- sale.order note-Field jetzt Html vorher Text

#### 08.06.2017
#### Version 1.0.4
##### [CHG]
- Zwischenstand

#### 08.06.2017
#### Version 1.0.3
##### [ADD]
- Beschreibung hinzugefügt

#### 06.06.2017
#### Version 1.0.2
##### [CHG]
- Zwischenstand

#### 24.05.2017
#### Version 1.0.1
##### [CHG]
- Quotation Templates Menüeintrag ausgebelendet

#### 19.05.2017
#### Version 1.0.0
##### [ADD]
- Port nach Odoo 10 begonnen