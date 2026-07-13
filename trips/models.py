import uuid
import json
from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    BUDGET_CHOICES = [
        ('budget', 'Budget'),
        ('mid', 'Mid-range'),
        ('luxury', 'Luxury'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    destination_name = models.CharField(max_length=150)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    traveler_count = models.PositiveIntegerField(default=2)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='mid')
    travel_styles = models.TextField(default='[]', help_text='JSON list of travel styles')
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_travel_styles(self):
        try:
            return json.loads(self.travel_styles)
        except (json.JSONDecodeError, TypeError):
            return []

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class ItineraryItem(models.Model):
    TIME_OF_DAY_CHOICES = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itinerary_items')
    day_number = models.PositiveIntegerField(default=1)
    time_of_day = models.CharField(max_length=20, choices=TIME_OF_DAY_CHOICES, default='MORNING')
    time_range = models.CharField(max_length=50, blank=True, default='')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField(max_length=500, blank=True, default='')
    transport_info = models.CharField(max_length=255, blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Day {self.day_number} {self.time_of_day}: {self.title}"

    class Meta:
        ordering = ['day_number', 'order']


class SavedTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_trips')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trip')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.trip.title}"
