from django.contrib import admin
from .models import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_station_alerts', 'low_water_notifications', 'dark_mode_preference', 'auto_refresh_dashboard')
