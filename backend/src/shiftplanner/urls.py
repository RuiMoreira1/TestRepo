"""shiftplanner api URL Configuration"""

from rest_framework import routers
from django.urls import include, path

from src.shiftplanner.views import (
    ServiceViewSet,
    StaffViewSet,
    ScheduleViewSet,
    ShiftViewSet,
    WorkstationViewSet,
)

router = routers.DefaultRouter()
router.register(r"service", ServiceViewSet)
router.register(r"staff", StaffViewSet)
router.register(r"schedule", ScheduleViewSet, basename="schedule")
router.register(r"shift", ShiftViewSet, basename="shift")
router.register(r"workstation", WorkstationViewSet, basename="workstation")

urlpatterns = [
    path("", include(router.urls)),
    path("services", ServiceViewSet.as_view({"get": "list"})),
    path("generate/<int:number_days>", ScheduleViewSet.as_view({"post": "create"})),
]
