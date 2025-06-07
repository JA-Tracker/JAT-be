from django.core.management.base import BaseCommand
from app.models import User

class Command(BaseCommand):
    help = 'Promotes Django superusers to have the ADMIN role'

    def handle(self, *args, **options):
        # Get all superusers
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(self.style.WARNING('No superusers found.'))
            return
        
        # Update each superuser to have the ADMIN role
        count = 0
        for user in superusers:
            if user.role != User.Role.ADMIN:
                user.role = User.Role.ADMIN
                user.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated user {user.email} to have ADMIN role.'))
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('All superusers already have the ADMIN role.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} superuser(s) to have the ADMIN role.')) 