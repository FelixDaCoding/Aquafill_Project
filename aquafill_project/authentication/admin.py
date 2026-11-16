from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institutional_email', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'institutional_email')
