# pylint: disable=no-member
"""shiftplanner Unit Tests"""

import datetime
import pytz
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.shiftplanner.models import (
    Shift,
    Allocation,
    Staff,
    Workstation,
    ServiceManager,
)

# Create your tests here.
class ScheduleTestCase(APITestCase):
    """Test Case for Schedule Operations"""

    def setUp(self):
        """Setup the test case by creating shifts, staff and allocations"""
        service_manager = ServiceManager.objects.create(
            name="service1", email="test_ServiceManager@ds.com"
        )

        n_workers_per_shift = 2
        shift_list = self.setup_create_shifts(0, service_manager, n_workers_per_shift)
        staff_list = self.setup_create_staff(0, service_manager)
        self.setup_allocate_schedules(shift_list, staff_list, n_workers_per_shift)

        # Create repeated service, to make sure shedules are filtered by service
        service_manager = ServiceManager.objects.create(
            name="service2", email="test_ServiceManager2@ds.com"
        )
        shift_list = self.setup_create_shifts(1, service_manager, n_workers_per_shift)
        staff_list = self.setup_create_staff(1, service_manager)
        self.setup_allocate_schedules(shift_list, staff_list, n_workers_per_shift)

    def setup_create_shifts(self, identifier, service_manager, n_workers_per_shift):
        """Create test shifts"""
        workstation = Workstation.objects.create(
            role=f"test_role{identifier}", service_manager=service_manager
        )

        start_time = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        delta = datetime.timedelta(hours=8)
        shift_list = []
        for i in range(6):
            shift = Shift.objects.create(
                id=i + 1 + identifier * 6,
                start_timestamp=start_time,
                duration=delta,
                number_of_workers=n_workers_per_shift,
                workstation=workstation,
            )
            shift_list.append(shift)
            start_time = start_time + delta
        return shift_list

    def setup_create_staff(self, identifier, service_manager):
        """Create test staff"""
        staff_list = []
        for i in range(8):
            staff = Staff.objects.create(
                name=f"name{i}",
                email=f"e{i}{identifier}@ds.com",
                staff_number=i + identifier * 8,
                service_manager=service_manager,
            )
            staff_list.append(staff)
        return staff_list

    def setup_allocate_schedules(self, shift_list, staff_list, n_workers_per_shift):
        """Create test allocations"""
        # Setup allocations for first 4 shifts
        for i in range(4):
            for j in range(n_workers_per_shift):
                Allocation.objects.create(
                    schedule_name="schedule1",
                    shift=shift_list[i],
                    staff=staff_list[i * n_workers_per_shift + j],
                )
        self.allocations1 = {1: [0, 1], 2: [2, 3], 3: [4, 5], 4: [6, 7]}

        # Same allocations as in schedule 1 but in reverse order
        for i in range(4):
            for j in range(n_workers_per_shift):
                Allocation.objects.create(
                    schedule_name="schedule2",
                    shift=shift_list[i],
                    staff=staff_list[
                        len(staff_list) - (i * n_workers_per_shift + j) - 1
                    ],
                )
        self.allocations2 = {1: [7, 6], 2: [5, 4], 3: [3, 2], 4: [1, 0]}

        # Third schedule with different set of shifts
        Allocation.objects.create(
            schedule_name="schedule3", shift=shift_list[-2], staff=staff_list[0]
        )
        Allocation.objects.create(
            schedule_name="schedule3", shift=shift_list[-1], staff=staff_list[1]
        )
        self.allocations3 = {5: [0], 6: [1]}

    def test_get_all_schedules(self):
        """Test the retrieval of all schedules (from all services)"""
        url = reverse("schedule-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

        for i in range(0, 2):
            for j in range(0, 3):
                data = response.data[i * 3 + j]
                self.assertEqual(data["service"], f"service{i+1}")
                self.assertEqual(data["name"], f"schedule{3-j}")
                self.assertTrue(
                    len(data["shiftAllocations"]) <= 4
                    and len(data["shiftAllocations"]) >= 2
                )

    def test_get_schedules(self):
        """Test the retrieval of a list of schedules, within a service"""
        url = reverse("schedule-list")
        response = self.client.get(url, {"service": "service1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i, allocation in enumerate(
            [self.allocations3, self.allocations2, self.allocations1]
        ):
            self.validate_schedules(
                response.data[i], f"schedule{3-i}", "service1", allocation
            )

    def test_get_schedule(self):
        """Test the retrieval of a single schedule, within a service"""
        for i, allocation in enumerate(
            [self.allocations1, self.allocations2, self.allocations3]
        ):
            url = reverse("schedule-detail", args=[f"schedule{i+1}"])
            response = self.client.get(url, {"service": "service1"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.validate_schedules(
                response.data, f"schedule{i+1}", "service1", allocation
            )

    def test_missing_schedule(self):
        """Test the retrieval of a non-existent schedule"""
        url = reverse("schedule-detail", args=["schedule4"])
        response = self.client.get(url, {"service": "service1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_service(self):
        """Test the retrieval of a schedule, when no service parameter is sent"""
        url = reverse("schedule-detail", args=["schedule1"])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def validate_schedules(
        self, data, schedule_name, service_name, expected_allocations
    ):
        """Make sure the schedule data is correct according to
        a list of expected allocations"""
        self.assertEqual(data["name"], schedule_name)
        self.assertEqual(data["service"], service_name)
        self.assertEqual(len(data["shiftAllocations"]), len(expected_allocations))

        allocations = data["shiftAllocations"]
        for allocation in allocations:
            identifier = allocation["id"]
            self.assertIn(identifier, expected_allocations)
            for i, staff in enumerate(allocation["staff"]):
                self.assertEqual(
                    staff["staff_number"], expected_allocations[identifier][i]
                )
