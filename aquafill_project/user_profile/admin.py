from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'student_id', 'daily_water_target_ml', 'water_consumed_today_ml', 'updated_at')
    search_fields = ('user__username', 'student_id', 'department')
    list_filter = ('department',)
