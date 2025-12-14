from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Удаление дубликатов Google OAuth приложений'

    def handle(self, *args, **options):
        google_apps = SocialApp.objects.filter(provider='google')
        count = google_apps.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('⚠️ Google приложений не найдено'))
            return
        
        if count == 1:
            self.stdout.write(self.style.SUCCESS('✅ Дубликатов нет, всё в порядке'))
            return
        
        self.stdout.write(self.style.WARNING(f'Найдено {count} Google приложений'))
        
        # Оставляем первое, удаляем остальные
        first_app = google_apps.first()
        duplicates = google_apps.exclude(id=first_app.id)
        
        for app in duplicates:
            self.stdout.write(f'  Удаляем дубликат ID={app.id}: {app.name}')
            app.delete()
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Удалено дубликатов: {duplicates.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Оставлено приложение: {first_app.name} (ID={first_app.id})'))
