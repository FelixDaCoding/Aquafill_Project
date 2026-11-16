from django.conf import settings
from django.db import models


class UserSettings(models.Model):
    """
    Vertical slice model storing account preferences and notification settings.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings',
    )
    email_station_alerts = models.BooleanField(
        default=True,
        help_text='Receive email updates when water stations are refilled or serviced',
    )
    low_water_notifications = models.BooleanField(
        default=True,
        help_text='Receive alerts when stations in your department run low',
    )
    dark_mode_preference = models.BooleanField(
        default=False,
        help_text='Enable dark dashboard theme',
    )
    auto_refresh_dashboard = models.BooleanField(
        default=True,
        help_text='Auto-refresh live station statuses on the home screen every 60 seconds',
    )
    show_hydration_reminder = models.BooleanField(
        default=True,
        help_text='Show daily water intake reminder prompts',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'

    def __str__(self):
        return f'{self.user.username} Settings'
