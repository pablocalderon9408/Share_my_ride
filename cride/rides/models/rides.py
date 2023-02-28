"""Rides models."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CrideModel


class Ride(CrideModel):
    """Ride model."""

    offered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    offered_in = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)
    passengers = models.ManyToManyField('users.User', related_name='passengers')

    available_seats = models.PositiveSmallIntegerField(default=4)
    comments = models.TextField(blank=True)

    departure_location = models.CharField(max_length=140)
    departure_date = models.DateTimeField()

    arrival_location = models.CharField(max_length=140)
    arrival_date = models.DateTimeField()

    rating = models.FloatField(null=True)

    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Set to false when the ride is already done.'
    )

    is_offered = models.BooleanField(
        'offered status',
        default=False,
        help_text='Set to true when the ride is offered.'
    )

    def __str__(self):
        """Return ride and offered by."""
        return f'{self.offered_by} @ {self.offered_in}'

    class Meta:
        """Meta class."""

        ordering = ['-departure_date', '-arrival_date']
        unique_together = ('offered_by', 'departure_date', 'arrival_date')
