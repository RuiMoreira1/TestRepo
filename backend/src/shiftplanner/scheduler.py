""" Module to generate schedule """
from ortools.sat.python import cp_model


class Scheduler(cp_model.CpSolverSolutionCallback):
    """Scheduler class taking advantage of Google OrTools python library"""

    def __init__(self, service, num_days):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.staff = service.get_staff()
        self.shifts = service.get_shifts()
        self.num_days = num_days
        self.opt_vars = {}
        self.solutions = []
        self.solution_limit = 5
        self.solution_count = 0

    def incompatible(self, shift1, shift2):
        """Determines if shift1 and shift2 are incompatible"""
        # Staff cannot work in the next day if they worked at night
        night_shift = shift1.get_start_minutes() > shift1.get_end_minutes()

        # Verify if shift1 overlaps shift2
        # Staff cannot work two shifts in a row
        s2_start_time = (
            shift2.get_start_minutes()
            if shift1 < shift2
            else shift2.get_start_minutes() + 1440
        )
        overlapped_shifts = s2_start_time <= shift1.get_end_minutes()

        return night_shift or overlapped_shifts

    def calculate_avg_working_hours(self):
        """Returns the average working hours of each staff member"""
        daily_hours = 0
        for shift in self.shifts:
            daily_hours += shift.get_duration_minutes() * shift.number_of_workers

        return int((daily_hours * self.num_days / len(self.staff) + 0.5))

    def incompatible_shifts(self):
        """ "Returns a list with all the incompatible shifts"""
        incompatible_shift_pairs = []
        # (shift1, shift2, next_day in {0,1})
        # shift1 is incompatible with o shift2 of (0 -> same day / 1 -> next day)

        for ind1, shift1 in enumerate(self.shifts):
            for ind2, shift2 in enumerate(self.shifts):
                if self.incompatible(shift1, shift2):
                    incompatible_shift_pairs.append(
                        (ind1, ind2, 1 if shift1.different_days() else 0)
                    )

        return incompatible_shift_pairs

    def add_restrictions(self, model, threshold=480):
        """Adds the necessary restrictions to the model"""
        # Number of people working in shift s
        # must be exactly s.get_number_of_workers()
        for day in range(self.num_days):
            for shift, shift_obj in enumerate(self.shifts):
                people_per_shift = []
                for staff in range(len(self.staff)):
                    people_per_shift.append(self.opt_vars[(staff, day, shift)])
                model.Add(sum(people_per_shift) == shift_obj.number_of_workers)

        ##Try to balance working hours between staff
        avg = self.calculate_avg_working_hours()

        for staff in range(len(self.staff)):
            shift_per_staff = []
            for day in range(self.num_days):
                for shift, shift_obj in enumerate(self.shifts):
                    shift_per_staff.append(
                        (
                            self.opt_vars[(staff, day, shift)],
                            shift_obj.get_duration_minutes(),
                        )
                    )

            model.Add(
                (
                    sum(shift * duration for shift, duration in shift_per_staff)
                    >= avg - threshold
                )
            )
            model.Add(
                (
                    sum(shift * duration for shift, duration in shift_per_staff)
                    <= avg + threshold
                )
            )

        # Staff cannot work two shifts in a row
        # Staff cannot work in the next day if they worked at night
        incompatible_shift_pairs = self.incompatible_shifts()

        for shift1, shift2, next_day in incompatible_shift_pairs:
            for day in range(self.num_days):
                if next_day == 1 and day == self.num_days - 1:
                    continue
                for staff in range(len(self.staff)):
                    model.AddAtMostOne(
                        [
                            self.opt_vars[(staff, day, shift1)],
                            self.opt_vars[(staff, day + next_day, shift2)],
                        ]
                    )

    def create_model(self):
        """
        Creates a new model according to the specified
        attributes of the Schedule object
        """
        model = cp_model.CpModel()

        for staff in range(len(self.staff)):
            for day in range(self.num_days):
                for shift in range(len(self.shifts)):
                    self.opt_vars[(staff, day, shift)] = model.NewBoolVar(
                        f"{staff}-{day}-{shift}"
                    )
        return model

    def solve(self):
        """Generate schedules"""
        model = self.create_model()
        self.add_restrictions(model)

        solver = cp_model.CpSolver()
        solver.parameters.linearization_level = 0
        # Enumerate all solutions.
        solver.parameters.enumerate_all_solutions = True

        self.solution_count = 0
        solver.Solve(model, self)

    def on_solution_callback(self):
        """Saves the solution found"""
        self.solution_count += 1
        sol = {}
        for day in range(self.num_days):
            day_sol = {}
            for shift in range(len(self.shifts)):
                shift_list = []
                for staff in range(len(self.staff)):
                    if self.Value(self.opt_vars[(staff, day, shift)]):
                        shift_list.append(staff)
                day_sol[shift] = shift_list
            sol[day] = day_sol

        self.solutions.append(sol)

        if self.solution_count >= self.solution_limit:
            self.StopSearch()
