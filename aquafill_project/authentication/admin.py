from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Profile
from user_profile.models import UserProfile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Campus Identity & Role'
    verbose_name_plural = 'Campus Identity & Role'
    fk_name = 'user'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Hydration Telemetry Profile'
    verbose_name_plural = 'Hydration Telemetry Profile'
    fk_name = 'user'


# Unregister default User to register comprehensive AquaFill UserAdmin
admin.site.unregister(User)


@admin.register(User)
class AquaFillUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserProfileInline)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'campus_role_badge',
        'campus_department',
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')

    @admin.display(description='Campus Role')
    def campus_role_badge(self, obj):
        profile = getattr(obj, 'profile', None)
        if not profile:
            return mark_safe('<span style="color:#94A3B8;">Unassigned</span>')
        colors = {
            Profile.Role.STUDENT: ('#0369A1', '#F0F9FF', '#BAE6FD'),
            Profile.Role.FACULTY: ('#4338CA', '#EEF2FF', '#C7D2FE'),
            Profile.Role.FACILITY_STAFF: ('#047857', '#ECFDF5', '#A7F3D0'),
        }
        text_color, bg_color, border_color = colors.get(
            profile.role, ('#475569', '#F1F5F9', '#CBD5E1')
        )
        return format_html(
            '<span style="display:inline-block; padding:2px 8px; border-radius:999px; '
            'font-weight:700; font-size:11px; color:{}; background:{}; border:1px solid {};">'
            '{}</span>',
            text_color, bg_color, border_color, profile.get_role_display()
        )

    @admin.display(description='College / Dept')
    def campus_department(self, obj):
        details = getattr(obj, 'profile_details', None)
        if details and details.department:
            return details.department
        return mark_safe('<span style="color:#94A3B8;">—</span>')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institutional_email', 'role_badge', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'institutional_email')
    date_hierarchy = 'created_at'

    @admin.display(description='Role')
    def role_badge(self, obj):
        colors = {
            Profile.Role.STUDENT: ('#0369A1', '#F0F9FF', '#BAE6FD'),
            Profile.Role.FACULTY: ('#4338CA', '#EEF2FF', '#C7D2FE'),
            Profile.Role.FACILITY_STAFF: ('#047857', '#ECFDF5', '#A7F3D0'),
        }
        text_color, bg_color, border_color = colors.get(
            obj.role, ('#475569', '#F1F5F9', '#CBD5E1')
        )
        return format_html(
            '<span style="display:inline-block; padding:3px 10px; border-radius:999px; '
            'font-weight:700; font-size:11px; color:{}; background:{}; border:1px solid {};">'
            '{}</span>',
            text_color, bg_color, border_color, obj.get_role_display()
        )

    actions = ['set_role_student', 'set_role_faculty', 'set_role_facility_staff']

    @admin.action(description='Set selected roles to Student')
    def set_role_student(self, request, queryset):
        updated = queryset.update(role=Profile.Role.STUDENT)
        self.message_user(request, f'{updated} user(s) set to Student role.')

    @admin.action(description='Set selected roles to Faculty')
    def set_role_faculty(self, request, queryset):
        updated = queryset.update(role=Profile.Role.FACULTY)
        self.message_user(request, f'{updated} user(s) set to Faculty role.')

    @admin.action(description='Set selected roles to Facility Staff')
    def set_role_facility_staff(self, request, queryset):
        updated = queryset.update(role=Profile.Role.FACILITY_STAFF)
        self.message_user(request, f'{updated} user(s) set to Facility Staff role.')
