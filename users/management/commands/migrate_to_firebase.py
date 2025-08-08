from django.core.management.base import BaseCommand
from users.models import AlumniPortalUser

class Command(BaseCommand):
    help = 'Migrate existing Google OAuth users to Firebase'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )
    
    def handle(self, *args, **options):
        # Find users with Google sign-in method
        google_users = AlumniPortalUser.objects.filter(signInMethod='google')
        
        self.stdout.write(f"Found {google_users.count()} users with Google sign-in method")
        
        if options['dry_run']:
            self.stdout.write("DRY RUN - No changes will be made")
            for user in google_users:
                self.stdout.write(f"Would update: {user.email}")
        else:
            updated_count = google_users.update(signInMethod='firebase')
            self.stdout.write(
                self.style.SUCCESS(f"Successfully updated {updated_count} users to Firebase")
            )