from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os


class Command(BaseCommand):
    help = 'Полная очистка и пересоздание Google OAuth'

    def handle(self, *args, **options):
        # Удаляем ВСЕ Google приложения
        google_apps = SocialApp.objects.filter(provider='google')
        count = google_apps.count()
        
        if count > 0:
            self.stdout.write(f'Удаляем {count} Google приложений...')
            google_apps.delete()
            self.stdout.write(self.style.SUCCESS('✓ Все Google приложения удалены'))
        
        # Получаем текущий сайт
        site = Site.objects.get_current()
        self.stdout.write(f'Текущий сайт: {site.domain}')
        
        # Создаём ОДНО новое приложение
        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('❌ Переменные окружения GOOGLE_OAUTH_CLIENT_ID/GOOGLE_OAUTH_CLIENT_SECRET не заданы'))
            self.stdout.write(self.style.WARNING('Установите их в окружении перед запуском команды.'))
            return

        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        google_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Google OAuth создан заново (ID={google_app.id})'))
        self.stdout.write(self.style.SUCCESS(f'✅ Привязан к сайту: {site.domain}'))
        
        # Проверка
        total = SocialApp.objects.filter(provider='google').count()
        self.stdout.write(self.style.SUCCESS(f'✅ Всего Google приложений в БД: {total}'))
