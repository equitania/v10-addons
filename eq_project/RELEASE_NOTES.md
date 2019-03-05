## Modul eq_project

#### 05.03.2019
#### Version 1.0.68
##### CHG
- The Datetime fields in project.task are changed to Date type

#### 04.03.2019
#### Version 1.0.67
##### FIX
- Reports: Fix of Task-Report and changing hours to german decimal standard

#### 01.03.2019
#### Version 1.0.66
##### ADD
- optical changes on task reports project_task_report_extension & project_task_chatter_report_extension
- German translation

#### 25.02.2019
#### Version 1.0.65
##### ADD/FIX
- Added invoice_id when timesheet line is created from widget weekly_timesheet
- On change of project_id in account_analytic_line, start and end time are equal to 0.0

#### 22.02.2019
#### Version 1.0.64
##### CHG
- Group group_no_one removed from task_id field in issue form view

#### 22.02.2019
#### Version 1.0.63
##### FIX
- Added task_id invisible in the Issue Timesheet page, for correct progress calculation

#### 21.02.2019
#### Version 1.0.62
##### FIX
- Disable changing of the start date if account.analytic.line id already exist

#### 21.02.2019
#### Version 1.0.61
##### FIX
- Changed sequence of the tree and form view in task and issue Timesheet
- Overrided unlink function in account.invoice.line for unlink the invoice_id in account.analytic.line

#### 21.02.2019
#### Version 1.0.60
##### FIX
- changed field for users on timesheet reports

#### 21.02.2019
#### Version 1.0.59
##### CHG
- Changed action and views of Timesheet smart and kanban buttons in Project

#### 20.02.2019
#### Version 1.0.58
##### CHG / FIX
- Removed filters and changed domain to My Timesheet filter
- Changed form views of task and issue timesheet
- Changed view for Activities, because of error

#### 20.02.2019
#### Version 1.0.57
##### CHG / FIX
- fix a german translation
- report for tasks (non-final)

#### 19.02.2019
#### Version 1.0.56
##### CHG / ADD
- timesheet reports (add new EQ version)
- changes in view for hr_timesheet_sheet.sheet
- Removed invoice_id from task and issue timesheets, added eq_time_invoice

#### 19.02.2019
#### Version 1.0.55
##### CHG
- Same tree, form and search views for Activities and Project/Timesheet

#### 19.02.2019
#### Version 1.0.54
##### CHG
- Changed order by id in account.analytic.line

#### 18.02.2019
#### Version 1.0.53
##### CHG
- Added hr_timesheet_task in dependencies
- Added domain move_id = False and removed filter Timesheet(all)
- Changed view for Activities

#### 18.02.2019
#### Version 1.0.52
##### CHG
- change view in report account extension.xml for person / user with break 

#### 15.02.2019
#### Version 1.0.51
##### CHG
- Changed search view for Activities

#### 14.02.2019
#### Version 1.0.50
##### CHG
- Changed fields in Timesheet search view and translation name

#### 14.02.2019
#### Version 1.0.49
##### CHG  
- user_id and project_id readonly when invoice_id is set

#### 14.02.2019
#### Version 1.0.48
##### CHG  
- Changed project, project issue and project task view
- Added translation

#### 12.02.2019
#### Version 1.0.47
##### FIX  
- Clean up project's timesheet menus and views 

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