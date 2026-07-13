from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.URLField(blank=True, default='')
    bio = models.TextField(blank=True, default='')
    miles_covered = models.PositiveIntegerField(default=0)
    trips_count = models.PositiveIntegerField(default=0)
    membership_year = models.PositiveIntegerField(default=2024)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"Profile of {self.user.username}"


class UserPreference(models.Model):
    BUDGET_CHOICES = [
        ('budget', 'Budget'),
        ('mid', 'Mid-range'),
        ('luxury', 'Luxury'),
    ]
    PACE_CHOICES = [
        ('leisurely', 'Leisurely (Relaxed & slow)'),
        ('moderate', 'Moderate'),
        ('fast', 'Fast-paced'),
    ]
    ACCOMMODATION_CHOICES = [
        ('hotel', 'Hotel'),
        ('hostel', 'Hostel'),
        ('resort', 'Resort'),
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    budget_preference = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='mid')
    travel_styles = models.TextField(
        default='[]',
        help_text='JSON list of selected travel styles e.g. ["Adventure","Cultural"]'
    )
    pace_of_travel = models.CharField(max_length=20, choices=PACE_CHOICES, default='moderate')
    accommodation_preference = models.CharField(max_length=30, choices=ACCOMMODATION_CHOICES, default='hotel')
    dietary_requirements = models.CharField(max_length=200, blank=True, default='')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)

    def get_travel_styles(self):
        try:
            return json.loads(self.travel_styles)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_travel_styles(self, styles_list):
        self.travel_styles = json.dumps(styles_list)

    def __str__(self):
        return f"Preferences of {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile_and_preferences(sender, instance, created, **kwargs):
    """Automatically create UserProfile and UserPreference on new user creation."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserPreference.objects.get_or_create(user=instance)
