# admin panel configuration
from django.contrib import admin
from .models import MoodEntry, Resource


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


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('category', 'title')
