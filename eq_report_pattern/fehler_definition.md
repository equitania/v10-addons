Folgender code macht den Menüeintrag "Quotation Templates" unsichtbar.

<record model="ir.ui.menu" id="website_quote.menu_sale_quote_template">
    <field name="action" eval="False"/>
</record>

Dieser wird durch einen Eintrag ersetz, der auf ein eigenes Template zeigt.

In diesem Template wurde folgende Zeile
<field name="product_id" on_change="on_change_product_id(product_id)"/>

so verändert

<field name="product_id" on_change="_onchange_product_id"/>

Das Fehlverhalten tritt auf wenn man speichern bzw eine neue Position erstellen möchte.
Im Fall des neuen Eintrags passiert nichts und clickt man auf SPEICHERN wird die Position nicht gespeichert.

Die Maske ist über Konfiguration -> Verkauf -> Dokumentenvorlage zu erreichen

![alt tag](images/fehler_definition.png)