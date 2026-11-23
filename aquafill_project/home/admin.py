from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import RefillReport, WaterStation

# Custom branding for the AquaFill Django Admin site
admin.site.site_header = 'AquaFill CIT-U Operations & Facility Admin'
admin.site.site_title = 'AquaFill Admin Portal'
admin.site.index_title = 'Campus Hydration & Maintenance Management'


class RefillReportInline(admin.TabularInline):
    """
    Inline maintenance and refill incident reports shown directly inside
    the WaterStation admin change view.
    """
    model = RefillReport
    extra = 0
    can_delete = False
    fields = ('reported_by', 'issue_type', 'status', 'notes', 'created_at', 'resolved_at')
    readonly_fields = ('created_at', 'resolved_at')
    show_change_link = True


@admin.register(WaterStation)
class WaterStationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'building',
        'floor',
        'status',
        'level_meter',
        'temperature_display',
        'total_dispensed_liters',
        'last_refilled_at',
    )
    list_filter = ('status', 'building')
    search_fields = ('name', 'building', 'floor')
    list_editable = ('status',)
    date_hierarchy = 'last_refilled_at'
    inlines = [RefillReportInline]

    fieldsets = (
        ('Station Identity & Location', {
            'fields': ('name', 'building', 'floor')
        }),
        ('Operational Telemetry', {
            'fields': ('status', 'capacity_liters', 'current_level_percentage', 'temperature_celsius')
        }),
        ('Cumulative Metrics & Logs', {
            'fields': ('total_dispensed_liters', 'last_refilled_at', 'created_at')
        }),
    )
    readonly_fields = ('created_at',)

    @admin.display(description='Water Supply Level')
    def level_meter(self, obj):
        level = obj.current_level_percentage
        if level >= 40:
            bar_color = '#0284C7'
        elif level >= 15:
            bar_color = '#F59E0B'
        else:
            bar_color = '#EF4444'

        return format_html(
            '<div style="width:130px; display:inline-block; vertical-align:middle;">'
            '  <div style="display:flex; justify-content:space-between; font-size:10.5px; font-weight:700; margin-bottom:2px;">'
            '    <span>{}%</span><span>({}L)</span>'
            '  </div>'
            '  <div style="background:#E2E8F0; border-radius:999px; height:8px; overflow:hidden;">'
            '    <div style="background:{}; width:{}%; height:8px; border-radius:999px;"></div>'
            '  </div>'
            '</div>',
            level, obj.capacity_liters, bar_color, min(100, level)
        )

    @admin.display(description='Chilled Temp')
    def temperature_display(self, obj):
        temp = obj.temperature_celsius
        icon = '❄️' if temp <= 12.0 else '🌡️'
        temp_str = f'{temp:.1f} °C'
        return format_html('<span style="font-weight:600;">{} {}</span>', icon, temp_str)

    # Custom Admin Actions
    actions = ['mark_as_online_full', 'mark_as_maintenance', 'mark_as_low_water']

    @admin.action(description='Mark selected stations as 100 percent Full and Online')
    def mark_as_online_full(self, request, queryset):
        updated = queryset.update(
            status=WaterStation.Status.ONLINE,
            current_level_percentage=100,
            last_refilled_at=timezone.now(),
        )
        self.message_user(request, f'Successfully marked {updated} station(s) 100% Full and Online.')

    @admin.action(description='Flag selected stations as Under Maintenance')
    def mark_as_maintenance(self, request, queryset):
        updated = queryset.update(status=WaterStation.Status.MAINTENANCE)
        self.message_user(request, f'{updated} station(s) set to Under Maintenance.')

    @admin.action(description='Flag selected stations as Low Supply Alert (under 15 percent)')
    def mark_as_low_water(self, request, queryset):
        updated = queryset.update(status=WaterStation.Status.LOW_WATER)
        self.message_user(request, f'{updated} station(s) flagged as Low Supply.')


@admin.register(RefillReport)
class RefillReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'station',
        'reported_by',
        'issue_type',
        'status',
        'notes_preview',
        'created_at',
        'resolved_at',
    )
    list_filter = ('status', 'issue_type', 'created_at', 'station__building')
    search_fields = ('station__name', 'station__building', 'reported_by__username', 'reported_by__email', 'notes')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Incident Information', {
            'fields': ('station', 'reported_by', 'issue_type', 'notes')
        }),
        ('Dispatch & Resolution', {
            'fields': ('status', 'created_at', 'resolved_at')
        }),
    )
    readonly_fields = ('created_at',)

    @admin.display(description='Notes / Landmark')
    def notes_preview(self, obj):
        if not obj.notes:
            return mark_safe('<span style="color:#94A3B8; font-style:italic;">No notes provided</span>')
        trimmed = (obj.notes[:50] + '...') if len(obj.notes) > 50 else obj.notes
        return trimmed

    actions = ['mark_as_resolved', 'mark_as_in_progress']

    @admin.action(description='Mark selected reports as Resolved and Dispatched')
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(
            status=RefillReport.ReportStatus.RESOLVED,
            resolved_at=timezone.now(),
        )
        self.message_user(request, f'{updated} incident report(s) marked as Resolved.')

    @admin.action(description='Mark selected reports as Staff Dispatched / In-Progress')
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status=RefillReport.ReportStatus.IN_PROGRESS)
        self.message_user(request, f'{updated} incident report(s) set to In Progress.')
