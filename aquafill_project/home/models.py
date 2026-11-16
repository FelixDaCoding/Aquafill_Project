from django.conf import settings
from django.db import models
from django.utils import timezone


class WaterStation(models.Model):
    """
    Campus water dispenser station model tracking telemetry, location, and operational status.
    """
    class Status(models.TextChoices):
        ONLINE = 'ONLINE', 'Online & Operational'
        LOW_WATER = 'LOW_WATER', 'Low Supply (< 15%)'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'
        OFFLINE = 'OFFLINE', 'Offline / Out of Service'

    name = models.CharField(max_length=100, help_text='Station Identifier, e.g. Station CEA-101')
    building = models.CharField(max_length=100, help_text='Campus Building, e.g. Engineering Hall')
    floor = models.CharField(max_length=50, help_text='Floor or Wing, e.g. 1st Floor East Wing')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONLINE)
    capacity_liters = models.FloatField(default=19.0, help_text='Total tank capacity in liters')
    current_level_percentage = models.PositiveIntegerField(default=85, help_text='Current level 0-100%')
    temperature_celsius = models.FloatField(default=9.2, help_text='Chilled water temperature (°C)')
    total_dispensed_liters = models.FloatField(default=1250.0, help_text='Cumulative liters dispensed')
    last_refilled_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['building', 'name']
        verbose_name = 'Campus Water Station'
        verbose_name_plural = 'Campus Water Stations'

    def __str__(self):
        return f'{self.name} - {self.building} ({self.get_status_display()})'

    @property
    def is_operational(self):
        return self.status in [self.Status.ONLINE, self.Status.LOW_WATER]

    @property
    def level_badge_color(self):
        if self.current_level_percentage > 40:
            return 'teal'
        elif self.current_level_percentage > 15:
            return 'amber'
        return 'rose'


class RefillReport(models.Model):
    """
    User-submitted maintenance and refill incident reports.
    """
    class IssueType(models.TextChoices):
        EMPTY = 'EMPTY', 'Water Tank Empty / Needs Refill'
        WARM = 'WARM', 'Chiller Not Cooling Water'
        LEAK = 'LEAK', 'Dispenser Faucet Leaking'
        FILTER = 'FILTER', 'Filter Replacement Needed'
        OTHER = 'OTHER', 'Other Station Issue'

    class ReportStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Facility Action'
        IN_PROGRESS = 'IN_PROGRESS', 'Staff Dispatched'
        RESOLVED = 'RESOLVED', 'Resolved / Refilled'

    station = models.ForeignKey(WaterStation, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refill_reports')
    issue_type = models.CharField(max_length=20, choices=IssueType.choices, default=IssueType.EMPTY)
    notes = models.TextField(blank=True, help_text='Additional details about the issue')
    status = models.CharField(max_length=20, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Station Maintenance Report'
        verbose_name_plural = 'Station Maintenance Reports'

    def __str__(self):
        return f'Report #{self.id} for {self.station.name} ({self.get_status_display()})'
