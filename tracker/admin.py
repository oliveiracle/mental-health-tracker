from django.contrib import admin
from .models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood_score', 'created_at')
    list_filter = ('date', 'mood_score')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)
