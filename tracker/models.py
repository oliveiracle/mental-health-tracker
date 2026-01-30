from django.db import models
from django.contrib.auth.models import User


class MoodEntry(models.Model):
    """
    Model to store user's daily mood entries
    """
    MOOD_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Below Average'),
        (4, 'Slightly Below Average'),
        (5, 'Average'),
        (6, 'Slightly Above Average'),
        (7, 'Good'),
        (8, 'Very Good'),
        (9, 'Great'),
        (10, 'Excellent'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mood_entries'
    )
    date = models.DateField(auto_now_add=True)
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Mood Entries'
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - Score: {self.mood_score}"
