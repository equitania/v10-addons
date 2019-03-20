## Modul eq_base_report

#### 20.03.2019
#### Version 1.0.42
##### IMP
- Reportstyles: further improvement of shipping address

#### 20.03.2019
#### Version 1.0.41
##### IMP
- Report sending address now has a limitation in width and breaks into a second line, to still be in the view-window of letters.
- Report second page, Header on second and following pages will have correct positions

#### 13.03.2019
#### Version 1.0.40
##### CHG
- Switch to WKHTMLtoPDF 0.12.5 ... Reports and Reportstyles!

#### 18.02.2019
#### Version 1.0.39
##### CHG
- Internal Standard Report: Changing top border color from green to black
- New Paperformat: Landscape

#### 17.12.2018
#### Version 1.0.38
##### ADD
- Report: overdue payment improvements

#### 13.12.2018
#### Version 1.0.37
##### IMP
- intern basic report header, set new max-sizes for reportlogo and using a smaller font size for own company 

#### 12.12.2018
#### Version 1.0.36
##### CHG
- Report Footer Style: setting a smaller padding for footer columns, to get the same usable space as before the odoo DPI changes been made

#### 04.12.2018
#### Version 1.0.35
##### FIX
- Fixing Text and Logo Size on Reports, after odoo changed behaviour of DPI on Reports

#### 19.09.2018
#### Version 1.0.34
##### FIX
- missing german translations

#### 16.08.2018
#### Version 1.0.33
##### ADD
- Included new css class for optional text-colors in sale orders

#### 12.06.2018
#### Version 1.0.32
##### ADD
- eq_house_no into the report-Footer

#### 17.05.2018
#### Version 1.0.31
##### CHG
- add css class for eq_hr_time_management

#### 07.03.2018
#### Version 1.0.30
##### CHG
- Print Statements entfernt

#### 01.03.2018
#### Version 1.0.29
##### FIX
- reformat_string Funktion überarbeitet, welche bei einem negativen Wert noch einen Punkt vor den Zahlenwert gesetzt hat.

#### 09.02.2017
#### Version 1.0.28
##### FIX
- (VW-148) Reportstyle: Informationsblock oben rechts in Reports haben nun keine Padding-left mehr, dadurch ist der Block korrekt ausgerichtet zum Report-Logo

#### 24.01.2017
#### Version 1.0.27
##### IMP
- Diverse Anpassungen am Header, Footer & Styles:
  - Reportfooter für Standard Report Dokumente wird nun durch den Equitania Footer ersetzt
  - Reportheader für Standard Reports, welche z.B. noch von Online Website Angeboten angesprochen werden, werden nun durch eine optimierte Version erstzt und beinhalten weiterhin die Adresse der Firma
  - Repoststyles haben nun Definitionen für H1 bis h5 in der Schriftgröße


#### 17.01.2017
#### Version 1.0.26
##### IMP
- Reportfooter: Umbruch nach einer Bank erzwingen. Notwendig wenn man 2 Bankkonten angegeben hat.

#### 16.01.2017
#### Version 1.0.25
##### CHG
- Schriftfarbe für internen Reportheader auf schwarz geändert

#### 16.01.2017
#### Version 1.0.24
##### ADD
- Report Papierformat für interne Dokumente erstellt

#### 19.12.2017
#### Version 1.0.23
##### CHG
- Übersetzung für Kopfdaten von Angeboten angepasst

#### 19.12.2017
#### Version 1.0.22
##### CHG
- Reportstyle für Tabellen mit der Klasse "active" auf Tabellenzeile haben nun einen grauen Hintergrund (Anpassung für Sektionen)


#### 16.11.2017
#### Version 1.0.21
##### CHG
- Modul zu "Ausdrucke Basis" umbenannt

#### 08.08.2017
#### Version 1.0.20
##### IMP
- Erweiterung der Helperklasse um neue Funktion für optionale Produkte, VEP-138, eq_sale: Optionale Produkte, falsche Zwischensumme

#### 04.08.2017
#### Version 1.0.19
##### FIX
- Report Style: Schriftgrößen von PT auf PX umgestellt, damit die Version WKTHMLTOPDF 0.12.2.1 die PDF richtig rendert

#### 02.08.2017
#### Version 1.0.18
##### CHG
- Lieferschein-Kopf: Daten für Seite2+ nun enthalten

#### 01.08.2017
#### Version 1.0.17
##### CHG
- Lieferschein-Kopf: Vorerst den Infotext ausgeblendet

#### 28.07.2017
#### Version 1.0.16
##### CHG
- Modulbeschreibung erweitert

#### 26.07.2017
#### Version 1.0.15
##### CHG
- Neue Klasse mit Hilfsfunktionen für Reports


#### 04.07.2017
#### Version 1.0.14
##### ADD
- Report Header/Footer Erweiterung: Erweiterung der Logik für die Sichtbarkeit von Elementen auf 1. Seite, letzte Seite, alle außer 1. Seite, alle außer letzte Seite
- Hinzufügen von Textcontainern für Angebote und Rechnungen, welche ab der 2. Seite angezeigt werden (z.B. Kundennummer, Datum etc)

#### 28.06.2017
#### Version 1.0.13
##### CHG
- Schriftgröße von EM auf PT umgestellt; Hintergrundstyle für Sektionen

#### 26.06.2017
#### Version 1.0.12
##### CHG
- Graue Hintergrundfarbe für Auftragszeilen entfernt

#### 23.06.2017
#### Version 1.0.11
##### IMP
- Papierabstände in andere CSS Klasse verschoben

#### 23.06.2017
#### Version 1.0.10
##### CHG
- Footer nun mit equitania CEO Felder

#### 23.06.2017
#### Version 1.0.9
##### IMP
- Hinweis für das Reportlogo, wenn dieses noch nicht konfiguriert(hochgeladen) wurde
- FIX für die Listendarstellung von HTML Kopf & Fußtext

#### 20.06.2017
#### Version 1.0.8
##### IMP
- Übersetzungen im Footer nach neuer Logik (für Seite: und CEO:)

#### 19.06.2017
#### Version 1.0.7
##### CHG
- Anpassungen für die Footer Erweiterung

#### 19.06.2017
#### Version 1.0.6
##### ADD
- Papier DIN A4 Format hinzugefügt

#### 19.06.2017
#### Version 1.0.5
##### IMP
- Schriftart auf Open Sans, und alternativ als Calibiri gesetzt

#### 19.06.2017
#### Version 1.0.4
##### CHG
- Verbesserungen an Schriftgröße und Footer

#### 16.06.2017
#### Version 1.0.3
##### CHG
- Schriftgröße und Reportlogo hinzugefügt

#### 14.06.2017
#### Version 1.0.2
##### ADD
- Footer und Header hinzugefügt für spätere Nutzung

#### 14.06.2017
#### Version 1.0.1
##### CHG
- Basis für Reportlogo fortgesetzt


#### 14.06.2017
#### Version 1.0.0
##### ADD
- Basis für die Report Styles erstellt, sowie Beginn mit dem Code für das EQ Report Logo
