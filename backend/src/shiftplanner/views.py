# pylint: disable=too-many-ancestors, no-member, invalid-name, unused-argument, too-few-public-methods
"""shiftplanner views Configuration"""
from rest_framework import viewsets, response, exceptions
from rest_framework.response import Response
from django.db.models import Prefetch

from src.shiftplanner.models import (
    ServiceManager,
    Allocation,
    Shift,
    Staff,
    Workstation,
)

from src.shiftplanner.scheduler import Scheduler

from src.shiftplanner.serializers import (
    ServiceSerializer,
    StaffSerializer,
    ShiftSerializer,
    ScheduleSerializer,
    WorkstationSerializer,
)

SERVICE_QUERY_PARAM = "service"
WORKSTATION_QUERY_NAME = "workstation"


class ServiceViewSet(viewsets.ModelViewSet):
    """Define Service views"""

    queryset = ServiceManager.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *_args, **kwargs):
        """List services"""
        services = ServiceManager.objects.all()
        services_list = []
        for service in services:
            serviceSerializer = ServiceSerializer(service)
            workstations = serviceSerializer.get_workstations_len()
            staff = serviceSerializer.get_staff_len()
            services_list.append(
                {
                    "id": service.id,
                    "name": service.name,
                    "number_workstations": workstations,
                    "number_staff": staff,
                }
            )

        return response.Response(services_list)


class StaffViewSet(viewsets.ModelViewSet):
    """Define Staff views"""

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    """Define Shift views"""

    serializer_class = ShiftSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned shifts to a given workstation.
        """

        queryset = Shift.objects.all()
        workstation = self.request.query_params.get(WORKSTATION_QUERY_NAME)
        if workstation is not None:
            queryset = queryset.filter(workstation=workstation)
        return queryset


class ScheduleViewSet(viewsets.ViewSet):
    """Define Schedule views"""

    def create(self, request, *_args, **kwargs):
        """Generates schedule"""
        number_days = kwargs["number_days"]
        if not request.user.is_authenticated:
            service = ServiceManager.objects.first()
            service_serializer = ServiceSerializer(service)
            solver = Scheduler(service_serializer, number_days)
            solver.solve()
            return Response(solver.solutions)
        return Response("")

    def list(self, request):
        """Get a list of all the schedules"""

        service_parameter = request.query_params.get(SERVICE_QUERY_PARAM)

        services = []
        if service_parameter is None:
            #  If a specific service is not specified, we must separate
            # the schedules by service since multiple services
            # can have schedules with the same name, but they're different entities
            for service_name in ServiceManager.objects.values("name"):
                services.append(service_name.get("name"))
        else:
            services = [service_parameter]

        data = []
        for service in services:
            for element in Allocation.objects.values(
                "schedule_name"
            ).distinct():  # For each schedule_name, get schedule data
                data.append(self._get_schedule_data(element["schedule_name"], service))

        serializer = ScheduleSerializer(data, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get a single schedule by name"""

        service = request.query_params.get(SERVICE_QUERY_PARAM)
        if (
            service is None
        ):  # If no service is specified, the schedule name is ambiguous
            raise exceptions.ValidationError("Service query parameter is required")

        serializer = ScheduleSerializer(self._get_schedule_data(pk, service))
        return response.Response(serializer.data)

    def _get_schedule_data(self, schedule_name, service):
        """Returns the data of a single schedule, given its name"""

        # Get allocations for the schedule
        allocations = Allocation.objects.filter(
            schedule_name=schedule_name,
            shift__workstation__service_manager__name=service,
        )
        if not allocations:
            raise exceptions.NotFound()

        # Get shifts allocated to said schedule
        shifts_in_schedule = Shift.objects.filter(pk__in=allocations.values("shift"))

        queryset = shifts_in_schedule.prefetch_related(
            Prefetch(
                "allocations",
                queryset=allocations.select_related("staff"),
                to_attr="filtered_allocations",
            )
        )
        return {"name": schedule_name, "shiftAllocations": queryset, "service": service}


class WorkstationViewSet(viewsets.ModelViewSet):
    """Define Workstation views"""

    serializer_class = WorkstationSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned workstations to a given service.
        """
        queryset = Workstation.objects.all()
        service = self.request.query_params.get(SERVICE_QUERY_PARAM)
        if service is not None:
            queryset = queryset.filter(service_manager=service)
        return queryset
