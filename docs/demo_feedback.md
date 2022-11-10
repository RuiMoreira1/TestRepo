# Demos Feedback

## Demo 1 - 2022-10-27 - End of Sprint 1

-   In the staff page, show every attribute in the table.
-   Shift must be reusable, independent from the day of the week or month and number of workers, as that information should go to workstations.
-   Workstations may work every day, a given day of the week, from monday to friday or on a given day of the month.
-   A workstation may only have one shift or combination of shifts, and restrictions should be applied to it instead of a given set of hours.
-   "Day shift" should be redefined as a morning shift plus an afternoon shift.
-   Shifts and combinations of shifts should be user definable, but should also present default configurations.
-   The app should handle the case where schedule cannot be created, preferably by softening the constraints (restrictions should have a definable priority), but may also just report an error.
-   Define monthly holidays (needs to be user based because of regional holidays).
-   A person's deviation from shift's default working hours should be specified.
-   Display generated schedule in a table as a function of the workstation (priority for next sprint) and as a function of the staff.
-   People and shifts have an acronym to easily display on the schedule interface.

### Delivered features

Based on the PO's feedback, the SPOs concluded that the following features were delivered:

-   US[#42](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/42)
-   US[#22](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/22)
-   US[#15](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/15)
-   US[#16](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/16)
-   US[#19](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/19) (note that this user story refers to the creation only, and should not include the assignment of shift information, which days of the week the workstation works, etc., that were noted in this demo feedback. These are new functionalities that do not belong to this user story, and should instead be added to a new user story)
-   US[#21](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/21)
-   US[#41](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/41)
-   US[#17](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/17)
-   US[#18](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/18)

### How the product backlog should be adapted

-   Create user stories for the new functionalities requested by the PO in this demo feedback.
-   Separate the display of the schedule in a table as a function of the workstation and as a function of the staff into two user stories, since the first one should have higher priority.
