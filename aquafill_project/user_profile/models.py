from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    Vertical slice model storing extended profile details and hydration tracking.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_details',
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        default='College of Computer Studies',
        help_text='College or Administrative Department',
    )
    student_id = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text='Campus ID (e.g. 21-1234-567)',
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text='Mobile contact number',
    )
    bio = models.TextField(
        blank=True,
        default='Active AquaFill campus station user. Passionate about staying hydrated and sustainable water usage.',
    )
    daily_water_target_ml = models.PositiveIntegerField(
        default=2000,
        help_text='Daily hydration target in milliliters (ml)',
    )
    water_consumed_today_ml = models.PositiveIntegerField(
        default=850,
        help_text='Water logged today in milliliters (ml)',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Extended Profile'
        verbose_name_plural = 'User Extended Profiles'

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def hydration_percentage(self):
        if self.daily_water_target_ml > 0:
            return min(100, int((self.water_consumed_today_ml / self.daily_water_target_ml) * 100))
        return 0
