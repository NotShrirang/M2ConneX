from django.core.management.base import BaseCommand
from CODE.utils.recommendations import get_recommendation_engine
from users.models import AlumniPortalUser

class Command(BaseCommand):
    help = 'Build or rebuild FAISS recommendation index'

    def add_arguments(self, parser):
        parser.add_argument('--rebuild', action='store_true', help='Force rebuild of entire index')

    def handle(self, *args, **options):
        self.stdout.write('Building FAISS recommendation index...')
        
        engine = get_recommendation_engine()
        users = AlumniPortalUser.objects.filter(is_active=True, isVerified=True)
        
        self.stdout.write(f'Processing {users.count()} users...')
        
        for i, user in enumerate(users):
            try:
                engine.get_or_create_user_embedding(user, force_refresh=options['rebuild'])
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'Processed {i + 1}/{users.count()} users')
            except Exception as e:
                self.stderr.write(f'Error processing user {user.id}: {e}')
        
        engine.save_index()
        self.stdout.write(self.style.SUCCESS('FAISS index built successfully!'))