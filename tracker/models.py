# models for database tables
from django.db import models
from django.contrib.auth.models import User


# model for storing mood entries
class MoodEntry(models.Model):
    # choices for mood score (0 to 10)
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
    
    # link to user (each entry belongs to a user)
    # delete entries if user deleted
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mood_entries'
    )
    # automatically set date when created
    date = models.DateField(auto_now_add=True)
    # mood score 0-10
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    # optional notes
    notes = models.TextField(blank=True, null=True)
    # when entry was created
    created_at = models.DateTimeField(auto_now_add=True)
    # when entry was last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']  # show newest entries first
        verbose_name_plural = 'Mood Entries'  # proper plural name
    
    # string representation for admin panel
    def __str__(self):
        return (
            f"{self.user.username} - {self.date} - Score: {self.mood_score}"
        )
