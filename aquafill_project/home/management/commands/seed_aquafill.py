from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from authentication.models import Profile
from home.models import RefillReport, WaterStation
from user_profile.models import UserProfile
from user_settings.models import UserSettings


class Command(BaseCommand):
    help = 'Seeds initial campus water stations, sample users, and settings for AquaFill'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning AquaFill campus data seeding...'))

        stations_data = [
            {
                'name': 'CEA Main Station 1',
                'building': 'College of Engineering & Architecture',
                'floor': '1st Floor East Lobby',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 92,
                'temperature_celsius': 8.5,
                'total_dispensed_liters': 2450.0,
            },
            {
                'name': 'Science & Tech Dispenser',
                'building': 'Science Complex (ST Building)',
                'floor': '2nd Floor Biology Wing',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 68,
                'temperature_celsius': 9.0,
                'total_dispensed_liters': 1820.0,
            },
            {
                'name': 'University Library Station',
                'building': 'Learning Resource Center (LRC)',
                'floor': 'Ground Floor Quiet Study Area',
                'status': WaterStation.Status.LOW_WATER,
                'capacity_liters': 19.0,
                'current_level_percentage': 12,
                'temperature_celsius': 10.2,
                'total_dispensed_liters': 3100.0,
            },
            {
                'name': 'Student Pavilion Hydration Unit',
                'building': 'Student Activity Center (SAC)',
                'floor': 'Ground Floor Food Court',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 38.0,
                'current_level_percentage': 82,
                'temperature_celsius': 7.6,
                'total_dispensed_liters': 5600.0,
            },
            {
                'name': 'CCS Tech Lab Dispenser',
                'building': 'College of Computer Studies',
                'floor': '3rd Floor Networking Lab',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 55,
                'temperature_celsius': 8.9,
                'total_dispensed_liters': 1420.0,
            },
            {
                'name': 'Athletics Gym Station',
                'building': 'University Sports Arena',
                'floor': 'Main Court Concourse',
                'status': WaterStation.Status.MAINTENANCE,
                'capacity_liters': 38.0,
                'current_level_percentage': 5,
                'temperature_celsius': 23.5,
                'total_dispensed_liters': 4100.0,
            },
        ]

        created_count = 0
        for s_data in stations_data:
            station, created = WaterStation.objects.update_or_create(
                name=s_data['name'],
                defaults=s_data,
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(stations_data)} Water Stations ({created_count} newly created).'))

        # Ensure all existing users have Profile, UserProfile, and UserSettings
        for user in User.objects.all():
            Profile.objects.get_or_create(
                user=user,
                defaults={'institutional_email': f'{user.username}@cit.edu', 'role': Profile.Role.STUDENT}
            )
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'department': 'College of Computer Studies',
                    'student_id': f'22-{user.id:04d}-CIT',
                    'daily_water_target_ml': 2000,
                    'water_consumed_today_ml': 950,
                }
            )
            UserSettings.objects.get_or_create(user=user)

        self.stdout.write(self.style.SUCCESS('AquaFill database seeding completed successfully!'))
