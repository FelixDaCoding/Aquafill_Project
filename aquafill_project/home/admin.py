from django.contrib import admin
from .models import RefillReport, WaterStation


@admin.register(WaterStation)
class WaterStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'floor', 'status', 'current_level_percentage', 'temperature_celsius', 'last_refilled_at')
    list_filter = ('status', 'building')
    search_fields = ('name', 'building')


@admin.register(RefillReport)
class RefillReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'reported_by', 'issue_type', 'status', 'created_at')
    list_filter = ('issue_type', 'status')
    search_fields = ('station__name', 'reported_by__username', 'notes')
