# Factsheet for Team 2

## Sprint 0

This sprint our team was in charge of defining the Acceptance Tests for the Service's User Stories. With 14 stories, we needed to handle several possible scenarios for each one and make sure that they are easily understood by less technical people. Besides this, we also defined the deployment more rigorously, by using UML, as well as the architecture and components of the ideal final system.

### The four user stories that we are most proud of

As we only dealt with the Acceptance Tests for each one, we are proud of handling the most complex ones, with the most corner cases. These are:

-   [#19](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/19) (Wrote) - Acceptance Tests for adding a workstation
-   [#22](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/22) (Wrote) - Acceptance Tests for browsing schedules
-   [#29](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/29) (Wrote) - Acceptance Tests for updating a staff member's information
-   [#39](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/39) (Wrote) - Acceptance Tests for manual schedule swaps

### The four pull requests that we are most proud of

The best pull requests are the ones that include the work we developed during this sprint, which are:

-   [#8](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/8) (Implemented) - Created an initial prototype of a user story template
-   [#13](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/13) (Implemented) - Generated the deployment diagram for the project
-   [#46](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/46) (Implemented) - Generated the architecture and component diagrams for the project
-   [#47](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/47) (Implemented) - Created the architecture and design sections of our documentation, explaining the pros and cons of each decision.

### Four other contributions that we are especially proud of

Firstly, our team worked really hard to try and simplify the system as much as possible, reducing the complexity of the overall product but keeping loyal to the Product Owner's specifications.

To accompany this, we strived to maintain good communication between the different teams, and shared our progress as much as possible, so that everyone was up to the part. Also, we tried to give our feedback to other teams, in order to create a consistent vision of the final product.

Whilst developing the Acceptance Tests was our main focus, it was not the hardest part of this Sprint. Getting adjusted to the scale of the team and developing consistent practices among all was the biggest and most note-worthy challenge so far.

## Sprint 1

In this sprint our focus was fully on one big increment, which was generating the schedules for the staff. For now, it does not accept most restrictions, but it already implements a few, minor ones, like having a required number of staff members to each shift, and the existence of incompatible shifts. Besides this, we also developed a frontend for the user to be able to generate the schedules with ease, and we made strides in creating the first acceptance tests for the frontend, with tests for the schedule generation page. Finally, as a work item, we implemented the e-mail service for our backend which will, in the future, send the schedules to all staff members.

### The four user stories that we are most proud of

-   [#27](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/27) (Implemented) - Create an e-mail service for the backend
-   [#51](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/51) (Implemented) - Create a page for generating schedules on the frontend
-   [#52](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/52) (Implemented) - Create Acceptance Tests for the schedule generation page
-   [#53](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/issues/53) (Implemented) - Generate a schedule using Google's OR-Tools, with minor restrictions

### The four pull requests that we are most proud of

-   [#60](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/60) (Implemented) - Created an e-mail service for the backend with the Sendinblue API
-   [#116](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/116) (Implemented) - Create the frontend for the schedule generation in the project
-   [#119](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/119) (Implemented) - Created the schedule generation service using Google's OR-Tools, with some minor restrictions already implemented as well
-   [#127](https://github.com/FEUP-MEIC-DS-2022-1MEIC03/shift_planner_project/pull/127) (Implemented) - Created the first acceptance tests for the frontend, to the schedule generation page

### Four other contributions that we are especially proud of

-   Configured the acceptance tests for the frontend with jest-cucumber, so that everyone can write them with ease
-   Setup Jest so that it can also accept unit tests
-   Integrated the services well with other teams
-   Talked with the PO to get additional information regarding the schedule restrictions
