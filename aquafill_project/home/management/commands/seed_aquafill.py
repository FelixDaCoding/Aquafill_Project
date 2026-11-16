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
                'name': 'NGE East Lobby Hydration Hub',
                'building': 'NGE Building (Nicolas G. Escario)',
                'floor': '1st Floor • Near Room NGE-104',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 92,
                'temperature_celsius': 8.4,
                'total_dispensed_liters': 2450.0,
            },
            {
                'name': 'NGE Engineering Drafting Wing',
                'building': 'NGE Building (Nicolas G. Escario)',
                'floor': '3rd Floor • Near Room NGE-308',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 76,
                'temperature_celsius': 8.9,
                'total_dispensed_liters': 1980.0,
            },
            {
                'name': 'GLE CCS Innovation Hub Dispenser',
                'building': 'GLE Building (Gregorio L. Escario)',
                'floor': '3rd Floor • Near Room GLE-304',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 88,
                'temperature_celsius': 7.8,
                'total_dispensed_liters': 3120.0,
            },
            {
                'name': 'GLE Networking & AI Lab Station',
                'building': 'GLE Building (Gregorio L. Escario)',
                'floor': '5th Floor • Near Room GLE-502',
                'status': WaterStation.Status.LOW_WATER,
                'capacity_liters': 19.0,
                'current_level_percentage': 24,
                'temperature_celsius': 9.4,
                'total_dispensed_liters': 2640.0,
            },
            {
                'name': 'RTL Learning Resource Commons',
                'building': 'RTL Building (Rodolfo T. Lizares)',
                'floor': 'Ground Floor • Quiet Study Zone',
                'status': WaterStation.Status.LOW_WATER,
                'capacity_liters': 19.0,
                'current_level_percentage': 18,
                'temperature_celsius': 10.1,
                'total_dispensed_liters': 3410.0,
            },
            {
                'name': 'RTL Case Room Corridor Unit',
                'building': 'RTL Building (Rodolfo T. Lizares)',
                'floor': '2nd Floor • Near Room RTL-210',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 84,
                'temperature_celsius': 8.6,
                'total_dispensed_liters': 2190.0,
            },
            {
                'name': 'SAL Science & Nursing Wing',
                'building': 'SAL Building (Science & Allied)',
                'floor': '2nd Floor • Biology Lab Alcove',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 19.0,
                'current_level_percentage': 68,
                'temperature_celsius': 9.0,
                'total_dispensed_liters': 1820.0,
            },
            {
                'name': 'Main Admin & Student Center Unit',
                'building': 'Main / Admin Building',
                'floor': 'Ground Floor • Registrar Concourse',
                'status': WaterStation.Status.ONLINE,
                'capacity_liters': 38.0,
                'current_level_percentage': 95,
                'temperature_celsius': 7.5,
                'total_dispensed_liters': 5600.0,
            },
            {
                'name': 'Wildcats Gymnasium Hydration Unit',
                'building': 'Main / Admin Building',
                'floor': '1st Floor • Main Court Concourse',
                'status': WaterStation.Status.MAINTENANCE,
                'capacity_liters': 38.0,
                'current_level_percentage': 6,
                'temperature_celsius': 22.8,
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

        # Ensure default 'admin' user exists and all existing accounts have Admin/Superuser access
        admin_user, _ = User.objects.update_or_create(
            username='admin',
            defaults={'email': 'admin@cit.edu', 'is_staff': True, 'is_superuser': True},
        )
        admin_user.set_password('admin12345')
        admin_user.save()
        User.objects.all().update(is_staff=True, is_superuser=True)

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
