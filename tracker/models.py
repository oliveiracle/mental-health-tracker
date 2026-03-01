from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    # Choices for mood score (0 to 10)
    MOOD_CHOICES = [
        (0, 'Very Low'),
        (1, 'Low'),
        (2, 'Below Average'),
        (3, 'Slightly Below Average'),
        (4, 'Average'),
        (5, 'Slightly Above Average'),
        (6, 'Good'),
        (7, 'Very Good'),
        (8, 'Great'),
        (9, 'Excellent'),
        (10, 'Outstanding'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete mood entries if user is deleted
        related_name='mood_entries'
    )
    date = models.DateField(auto_now_add=True)  # Date of the entry
    mood_score = models.IntegerField(choices=MOOD_CHOICES)  # Mood score (0-10)
    notes = models.TextField(blank=True, null=True, max_length=500)  # Optional notes (max 500 chars)
    created_at = models.DateTimeField(auto_now_add=True)  # When entry was created
    updated_at = models.DateTimeField(auto_now=True)      # When entry was last updated

    class Meta:
        ordering = ['-date']  # Show newest entries first
        verbose_name_plural = 'Mood Entries'

    def __str__(self):
        return f"{self.user.username} - {self.date} - Score: {self.mood_score}"


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("adhd", "ADHD"),
        ("depression", "Depression"),
        ("anxiety", "Anxiety"),
        ("general", "General"),
    ]

    title = models.CharField(max_length=120)  # Resource title
    description = models.TextField()           # Short description
    link = models.URLField()                  # External link
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Resource category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "title"]
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title
