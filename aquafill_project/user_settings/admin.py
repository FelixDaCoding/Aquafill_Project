from django.contrib import admin
from .models import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email_station_alerts',
        'low_water_notifications',
        'auto_refresh_dashboard',
        'show_hydration_reminder',
        'updated_at',
    )
    list_editable = (
        'email_station_alerts',
        'low_water_notifications',
        'auto_refresh_dashboard',
        'show_hydration_reminder',
    )
    list_filter = (
        'email_station_alerts',
        'low_water_notifications',
        'auto_refresh_dashboard',
        'show_hydration_reminder',
    )
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('User Association', {
            'fields': ('user',)
        }),
        ('Alert & Dispatch Routing', {
            'fields': ('email_station_alerts', 'low_water_notifications')
        }),
        ('Dashboard Telemetry Experience', {
            'fields': ('auto_refresh_dashboard', 'show_hydration_reminder', 'dark_mode_preference', 'updated_at')
        }),
    )

    actions = ['enable_all_notifications', 'disable_all_notifications']

    @admin.action(description='Enable all alerts & dashboard telemetry features')
    def enable_all_notifications(self, request, queryset):
        updated = queryset.update(
            email_station_alerts=True,
            low_water_notifications=True,
            auto_refresh_dashboard=True,
            show_hydration_reminder=True,
        )
        self.message_user(request, f'Enabled all alerts and telemetry for {updated} user(s).')

    @admin.action(description='Mute/Disable email and low supply notifications')
    def disable_all_notifications(self, request, queryset):
        updated = queryset.update(
            email_station_alerts=False,
            low_water_notifications=False,
        )
        self.message_user(request, f'Muted alerts for {updated} user(s).')
