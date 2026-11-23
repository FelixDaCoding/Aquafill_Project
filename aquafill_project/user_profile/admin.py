from django.contrib import admin
from django.utils.html import format_html
# pyrefly: ignore [missing-import]
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'student_id',
        'hydration_progress',
        'daily_water_target_ml',
        'water_consumed_today_ml',
        'updated_at',
    )
    list_filter = ('department', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id', 'department', 'phone_number')
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('Campus Identity & Contact', {
            'fields': ('user', 'department', 'student_id', 'phone_number', 'bio')
        }),
        ('Daily Hydration Telemetry', {
            'fields': ('daily_water_target_ml', 'water_consumed_today_ml', 'updated_at')
        }),
    )

    @admin.display(description='Hydration Progress')
    def hydration_progress(self, obj):
        pct = obj.hydration_percentage
        bar_color = '#10B981' if pct >= 100 else ('#0284C7' if pct >= 50 else '#F59E0B')
        return format_html(
            '<div style="width:130px; display:inline-block; vertical-align:middle;">'
            '  <div style="display:flex; justify-content:space-between; font-size:10.5px; font-weight:700; margin-bottom:2px;">'
            '    <span>{}%</span><span>{}/{} ml</span>'
            '  </div>'
            '  <div style="background:#E2E8F0; border-radius:999px; height:8px; overflow:hidden;">'
            '    <div style="background:{}; width:{}%; height:8px; border-radius:999px;"></div>'
            '  </div>'
            '</div>',
            pct, obj.water_consumed_today_ml, obj.daily_water_target_ml, bar_color, min(100, pct)
        )

    actions = ['reset_daily_intake', 'set_target_2000ml', 'set_target_2500ml']

    @admin.action(description='Reset today consumed water to 0 ml')
    def reset_daily_intake(self, request, queryset):
        updated = queryset.update(water_consumed_today_ml=0)
        self.message_user(request, f'Reset water intake for {updated} profile(s).')

    @admin.action(description='Set daily target to 2,000 ml (Standard)')
    def set_target_2000ml(self, request, queryset):
        updated = queryset.update(daily_water_target_ml=2000)
        self.message_user(request, f'Updated {updated} profile(s) target to 2,000 ml.')

    @admin.action(description='Set daily target to 2,500 ml (Athletic)')
    def set_target_2500ml(self, request, queryset):
        updated = queryset.update(daily_water_target_ml=2500)
        self.message_user(request, f'Updated {updated} profile(s) target to 2,500 ml.')
