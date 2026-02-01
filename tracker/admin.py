# admin panel configuration
from django.contrib import admin
from .models import MoodEntry


# register MoodEntry model in admin panel
@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    # columns to show in list view
    list_display = ('user', 'date', 'mood_score', 'created_at')
    # filters in sidebar
    list_filter = ('date', 'mood_score')
    # search fields
    search_fields = ('user__username', 'notes')
    # fields that can't be edited
    readonly_fields = ('created_at', 'updated_at')
    # default ordering (newest first)
    ordering = ('-date',)
