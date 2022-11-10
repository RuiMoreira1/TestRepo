# pylint: disable=too-few-public-methods, disable=no-member
"""
Module that creates and manages the database tables
"""

# Create your models here.
from django.db import models

from django.db.models import Q


class User(models.Model):
    """
    Model to represent a user
    """

    email = models.CharField(unique=True, max_length=64)
    password = models.CharField(max_length=64)


class Admin(models.Model):
    """
    Model to represent an admin
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ServiceManager(models.Model):
    """
    Model to represent a service
    """

    email = models.CharField(unique=True, max_length=64)
    name = models.CharField(unique=True, max_length=64)


class Workstation(models.Model):
    """
    Model to represent a workstation
    """

    role = models.CharField(unique=True, max_length=64)
    service_manager = models.ForeignKey(
        ServiceManager, on_delete=models.CASCADE, default=""
    )


class Staff(models.Model):
    """
    Model to represent a staff member
    """

    name = models.CharField(max_length=64)
    email = models.CharField(unique=True, max_length=64)
    staff_number = models.IntegerField(unique=True)
    service_manager = models.ForeignKey(
        ServiceManager, on_delete=models.CASCADE, default=""
    )


class Shift(models.Model):
    """
    Model to represent a shift
    """

    start_timestamp = models.DateTimeField()
    duration = models.DurationField()
    number_of_workers = models.IntegerField()

    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class that defines constraints for the Shift model
        """

        constraints = [
            models.CheckConstraint(
                check=Q(number_of_workers__gt=0), name="check_min_number_of_workers"
            ),
        ]

    def get_start_minutes(self):
        """Returns the start hours in minutes"""
        return self.start_timestamp.hour * 60 + self.start_timestamp.minute

    def get_duration_minutes(self):
        """Returns the duration in minutes"""
        return self.duration.seconds // 60

    def get_end_minutes(self):
        """Returns the end hour in minutes"""
        return (self.get_start_minutes() + self.get_duration_minutes()) % (1440)

    def different_days(self):
        """Returns if the shift belongs to 2 days"""
        return self.get_start_minutes() > self.get_end_minutes()

    def __lt__(self, other):
        """Determines if the shift is less than other"""
        if self.get_start_minutes() == other.get_start_minutes():
            return (
                self.get_start_minutes() + self.get_duration_minutes()
                < other.get_start_minutes() + other.get_duration_minutes()
            )
        return self.get_start_minutes() < other.get_start_minutes()


class Allocation(models.Model):
    """
    Model to represent an allocation
    """

    schedule_name = models.CharField(max_length=64)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default="")
    shift = models.ForeignKey(
        Shift, on_delete=models.CASCADE, default="", related_name="allocations"
    )

    class Meta:
        """
        Meta class that defines constraints for the Allocation model
        """

        unique_together = [("staff", "shift")]


class CanWork(models.Model):
    """
    Model to represent the relation between Staff and Workstation
    """

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default="")
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE, default="")

    class Meta:
        """
        Meta class that defines constraints for the CanWork model
        """

        unique_together = [("staff", "workstation")]
