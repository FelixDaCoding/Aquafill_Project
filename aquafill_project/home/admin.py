from django.contrib import admin
from django.utils import timezone
from .models import RefillReport, WaterStation

# Customize Django Admin branding for CIT-U AquaFill
admin.site.site_header = 'AquaFill CIT-U Telemetry & Janitorial Admin'
admin.site.site_title = 'AquaFill Admin Console'
admin.site.index_title = 'Campus Hydration & Facilities Command Center'


@admin.register(WaterStation)
class WaterStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'floor', 'status', 'current_level_percentage', 'temperature_celsius', 'last_refilled_at')
    list_filter = ('status', 'building')
    search_fields = ('name', 'building', 'floor')
    list_editable = ('status', 'current_level_percentage')
    actions = ['mark_stations_refilled']

    @admin.action(description='Mark selected stations 100%% Refilled & Online')
    def mark_stations_refilled(self, request, queryset):
        updated = queryset.update(
            status=WaterStation.Status.ONLINE,
            current_level_percentage=100,
            last_refilled_at=timezone.now(),
        )
        self.message_user(request, f'{updated} station(s) marked 100% full and online.')


@admin.register(RefillReport)
class RefillReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'reported_by', 'issue_type', 'status', 'created_at')
    list_filter = ('issue_type', 'status')
    search_fields = ('station__name', 'reported_by__username', 'notes')
    list_editable = ('status',)
    actions = ['mark_reports_resolved']

    @admin.action(description='Mark selected reports as Resolved / Refilled')
    def mark_reports_resolved(self, request, queryset):
        updated = queryset.update(
            status=RefillReport.ReportStatus.RESOLVED,
            resolved_at=timezone.now(),
        )
        self.message_user(request, f'{updated} maintenance report(s) marked as resolved.')
