from django.db import models
import json


class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('City', 'City'),
        ('Nature', 'Nature'),
        ('Beach', 'Beach'),
        ('Culture', 'Culture'),
        ('Adventure', 'Adventure'),
        ('Food', 'Food'),
        ('Shopping', 'Shopping'),
        ('Wildlife', 'Wildlife'),
        ('Mountain', 'Mountain'),
        ('Island', 'Island'),
    ]

    name = models.CharField(max_length=120)
    country = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True, default='')
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    categories = models.TextField(
        default='[]',
        help_text='JSON list of categories, e.g. ["City","Culture"]'
    )
    image_url = models.URLField(max_length=500, blank=True, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    best_season = models.CharField(max_length=100, blank=True, default='Year-round')
    language = models.CharField(max_length=100, blank=True, default='')
    currency = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_categories(self):
        try:
            return json.loads(self.categories)
        except (json.JSONDecodeError, TypeError):
            return []

    def categories_display(self):
        return ' • '.join(self.get_categories())

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['-is_featured', '-rating']
