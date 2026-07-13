from django.db import models
from destinations.models import Destination


class HiddenGem(models.Model):
    CATEGORY_CHOICES = [
        ('Nature', 'Nature'),
        ('Culture', 'Culture'),
        ('Food', 'Food'),
        ('Architecture', 'Architecture'),
        ('Adventure', 'Adventure'),
        ('Spiritual', 'Spiritual'),
        ('Scenic', 'Scenic'),
    ]

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='hidden_gems',
        null=True, blank=True
    )
    name = models.CharField(max_length=150)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    image_url = models.URLField(max_length=500, blank=True, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    why_special = models.TextField(blank=True, default='')
    transport_info = models.CharField(max_length=255, blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Nature')
    location_label = models.CharField(max_length=200, blank=True, default='')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Hidden Gem)"

    class Meta:
        ordering = ['-rating']
