## Modul eq_project

#### 19.11.2018
#### Version 1.0.46
##### FIX   
- do not allow negative unit_amount.

#### 26.10.2018
#### Version 1.0.45
##### CHG   
- german translation for Activities 

#### 25.10.2018
#### Version 1.0.44
##### ADD
- Warning if duration field in account.analytic.line in negative time
- Added translation

#### 22.10.2018
#### Version 1.0.43
##### FIX
- remove dependency to project_timesheet_time_control

#### 28.09.2018
#### Version 1.0.42
##### FIX
- initialize task_obj

#### 26.09.2018
#### Version 1.0.41
##### FIX
- Overwrite given view to set the task_id in context.

#### 18.09.2018
#### Version 1.0.40
##### FIX
- Fixing report-line, when no responsible person is selected

#### 20.08.2018
#### Version 1.0.39
##### DEL
- delete domain from 1.0.38

#### 14.08.2018
#### Version 1.0.38
##### FIX
- Adding domain in issue_id field in onchange project_id function

#### 10.08.2018
#### Version 1.0.37
##### ADD
- add select product on line in account.analytic.line

#### 07.08.2018
#### Version 1.0.36
##### ADD
- unit_amount negative when invoice refund.
- select issue and task only from project.

#### 07.08.2018
#### Version 1.0.35
##### ADD
- adding eq_time_invoice into timesheet-report

#### 07.08.2018
#### Version 1.0.34
##### CHG
- change status of shown proceeds

#### 06.08.2018
#### Version 1.0.33
##### ADD
- new icon for contracts and proceeds.

#### 06.08.2018
#### Version 1.0.32
##### ADD
- Adding "invoiceable" column to the timesheet report
- Adding responsible Persons Name under the invoice description
- Changing Translations

#### 06.08.2018
#### Version 1.0.31
##### ADD
- add proceed to line

#### 06.08.2018
#### Version 1.0.30
##### ADD
- calculate refund and compute proceed - refund

#### 06.08.2018
#### Version 1.0.29
##### ADD
- add project proceeds smart button to project.project form view
- ignore invoice refunds in project proceeds

#### 06.08.2018
#### Version 1.0.28
##### ADD
- add contract smart button to project form view.

#### 03.08.2018
#### Version 1.0.27
##### ADD
- add invoice time to account.analytic.line

#### 18.07.2018
#### Version 1.0.26
##### ADD
- remove domain filter 'project_id' from account.analytic.line tree view.
- editable bottom in tree views

#### 13.07.2018
#### Version 1.0.25
##### ADD
- add domain to timesheet (all). Only timesheets without move_id will shown.

#### 13.07.2018
#### Version 1.0.24
##### ADD
- add invoice_refund functionality for eq_storno_flag

#### 06.07.2018
#### Version 1.0.23
##### ADD
- storno flag to account.analytic.line
- remove link to invoice when you cancel a invoice (in account.analytic.line)

#### 28.06.2018
#### Version 1.0.22
##### ADD
- add Timesheet (all) under search menu in project. 

#### 25.06.2018
#### Version 1.0.21
##### ADD
- add to_invoice to project_issue and project_task 

#### 16.04.2018
#### Version 1.0.20
##### ADD
- different project stages in project kanban view

#### 16.04.2018
#### Version 1.0.19
##### ADD
- add dependency to OCA-module 'project_parent'

#### 22.03.2018
#### Version 1.0.18
##### ADD
- Timesheet Report: improved the standard timesheet report with the projectname and projectno (if avaiblable).
As well as an signing-field under the project table

#### 09.03.2018
#### Version 1.0.17
##### ADD
- add time_start and time_stop at project.task timesheet
- add dependency

#### 05.03.2018
#### Version 1.0.16
##### ADD
- added a new icon

#### 07.02.2018
#### Version 1.0.15
##### CHG
- Defaultwert von Startdate wird ab jetzt als DateTime.Now gesetzt

#### 07.02.2018
#### Version 1.0.13
##### IMP
- Refactoring und Erweiterung der Dokumentation

#### 07.02.2018
#### Version 1.0.12
##### CHG/FIX
- diverse BUgFixes

#### 06.02.2018
#### Version 1.0.11
##### IMP
- Projekt Einstellungen: Entfernen der Enterprise-Information für Stundenzettel-App


#### 05.02.2018
#### Version 1.0.9
##### ADD
- Projekt nummern werden nicht mehr Überschrieben.
- startdatum & startzeit automatisch einnehmen.
- Produkt spalte in Zeiterfassung hinzugefügt.
- Übersetzung  angepasst

#### 05.02.2018
#### Version 1.0.8
##### ADD
- Berechnung angepasst.

#### 05.02.2018
#### Version 1.0.7
##### ADD
- ir_sequence.next_by_code() anstatt ir_sequence.get() (war deprecated)

#### 02.02.2018
#### Version 1.0.6
##### ADD
- Berechnungsfunction für die Zeiterfassung angepasst.
- Button eingesetzt für die automatische Generierung von Projekt_Nummer
- Erweiterung der Stufen_Ansicht für die Berechnung Option
- Anpassung Übersetzung
- Projektnummererzeugungsbutton -> Link
- Code dokumentiert

#### 02.02.2018
#### Version 1.0.5
##### ADD
- Reihenfolge, Arbeitszeit, Startdatum, Ablaufdatum und Berechnungsart werden jetzt auch außerhalb des Debugmodus eingeblendet.
- Übersetzung angepasst
- Filter überarbeitet und wieder einkommentiert.

#### 02.02.2018
#### Version 1.0.4
##### ADD
- Suche 'Projekt' => Erste Anzeige Kanban-View

#### 02.02.2018
#### Version 1.0.3
##### ADD
- Aufruf Projekte Suchen Maske, ruft jetzt die korrekte Formansicht auf.

#### 02.02.2018
#### Version 1.0.2
##### ADD
- Anpassung Kanban-View, einen Bindestrich zwischen Projektnamen und Nummer
- Verrechenbar wird automatisch gesetzt.

#### 01.02.2018
#### Version 1.0.1
##### ADD
- Initialer Commit