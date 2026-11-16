from django.core.management.base import BaseCommand
from django.db import connection
from home.models import WaterStation
from authentication.models import Profile


class Command(BaseCommand):
    help = 'Checks and verifies active database connection (Supabase PostgreSQL vs SQLite)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Checking database connectivity...'))

        vendor = connection.vendor
        db_settings = connection.settings_dict
        engine = db_settings.get('ENGINE', '')
        name = db_settings.get('NAME', '')
        host = db_settings.get('HOST', 'localhost')

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')
                cursor.fetchone()

            self.stdout.write(self.style.SUCCESS('[OK] Database connection test: OK (SELECT 1 succeeded)'))
            self.stdout.write(f'Database Vendor: {vendor}')
            self.stdout.write(f'Engine: {engine}')
            self.stdout.write(f'Host: {host}')
            self.stdout.write(f'Database: {name}')

            if 'postgresql' in engine or 'postgres' in vendor:
                self.stdout.write(self.style.SUCCESS('\n======================================================='))
                self.stdout.write(self.style.SUCCESS('[SUCCESS] CONNECTED TO SUPABASE POSTGRESQL!'))
                self.stdout.write(self.style.SUCCESS('======================================================='))
                self.stdout.write('Your migrations and operations are running against your cloud Supabase database.')
                self.stdout.write('Open Supabase -> Table Editor in your browser to inspect real-time records.')
            else:
                self.stdout.write(self.style.WARNING('\n======================================================='))
                self.stdout.write(self.style.WARNING('[NOTICE] RUNNING ON LOCAL SQLITE'))
                self.stdout.write(self.style.WARNING('======================================================='))
                self.stdout.write('Your application is operating smoothly on local SQLite.')
                self.stdout.write('To switch to Supabase PostgreSQL, set DATABASE_URL in your .env file and run:')
                self.stdout.write('  python manage.py migrate')
                self.stdout.write('  python manage.py seed_aquafill\n')

            station_count = WaterStation.objects.count()
            profile_count = Profile.objects.count()
            self.stdout.write(f'Active Records: {station_count} Water Stations, {profile_count} User Profiles.')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database Connection Failed: {e}'))
