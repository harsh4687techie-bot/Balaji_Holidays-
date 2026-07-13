from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Planning', 'Trip Planning'),
        ('Booking', 'Booking & Payments'),
        ('Safety', 'Safety & Support'),
    ]
    
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.question}"

    class Meta:
        ordering = ['category', 'question']
