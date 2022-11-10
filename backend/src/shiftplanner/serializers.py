# pylint: disable=too-few-public-methods, abstract-method, no-member, W0223
"""shiftplanner Serializers Configuration"""

from rest_framework import serializers
from src.shiftplanner.models import ServiceManager, Shift, Staff, Workstation


class ServiceSerializer(serializers.ModelSerializer):
    """Service Serializer"""

    class Meta:
        """Service Serializer Data"""

        model = ServiceManager
        fields = ("id", "name", "email")

    def get_staff(self):
        """Returns the staff of the service"""
        return [
            StaffSerializer(staff)
            for staff in Staff.objects.filter(service_manager=self.data["id"])
        ]

    def get_workstations(self):
        """Returns the workstations of the service"""
        return [
            WorkstationSerializer(workstation)
            for workstation in Workstation.objects.filter(
                service_manager=self.data["id"]
            )
        ]

    def get_shifts(self):
        """ "Returns the shifts of the service"""
        shifts = []
        for workstation in self.get_workstations():
            shifts += workstation.get_shifts()
        return shifts

    def get_workstations_len(self):
        """Service Workstations Length Data"""
        return len(list(Workstation.objects.filter(service_manager=self.data["id"])))

    def get_staff_len(self):
        """Service Staff Length Data"""
        return len(list(Staff.objects.filter(service_manager=self.data["id"])))


class StaffSerializer(serializers.ModelSerializer):
    """Staff Serializer"""

    class Meta:
        """Staff Serializer Data"""

        model = Staff
        fields = (
            "id",
            "staff_number",
            "name",
            "email",
            "service_manager",
        )


class ShiftSerializer(serializers.ModelSerializer):
    """Shift Serializer"""

    class Meta:
        """Shift Serializer Data"""

        model = Shift
        fields = "__all__"


class ShiftAllocationSerializer(ShiftSerializer):
    """Shift Allocation Serializer"""

    staff = serializers.SerializerMethodField(read_only=True)

    def get_staff(self, obj):
        """Get serialized data of staff allocated to this shift"""
        return [
            StaffSerializer(allocation.staff).data
            for allocation in obj.filtered_allocations
        ]


class ScheduleSerializer(serializers.Serializer):
    """Schedule Serializer"""

    name = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)
    shiftAllocations = ShiftAllocationSerializer(many=True, read_only=True)


class WorkstationSerializer(serializers.ModelSerializer):
    """Workstation Serializer"""

    class Meta:
        """Workstation Serializer Data"""

        model = Workstation
        fields = "__all__"

    def get_shifts(self):
        """ "Returns the shifts of the workstation"""
        return list(Shift.objects.filter(workstation=self.data["id"]))
