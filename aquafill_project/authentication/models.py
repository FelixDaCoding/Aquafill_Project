from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Extends Django's built-in User model with AquaFill-specific fields
    (institutional email + campus role) without needing a custom user model.
    """

    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        FACULTY = 'FACULTY', 'Faculty'
        FACILITY_STAFF = 'FACILITY_STAFF', 'Janitorial / Facility Staff'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    institutional_email = models.EmailField(
        unique=True,
        help_text='Official campus/institutional email address.',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'AquaFill Profile'
        verbose_name_plural = 'AquaFill Profiles'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
