import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

load_dotenv()


class Command(BaseCommand):
    help = 'Полная очистка и пересоздание Google OAuth'

    def handle(self, *args, **options):
        # Get credentials from environment
        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
        secret = os.getenv('GOOGLE_OAUTH_SECRET_KEY', '')
        
        if not client_id or not secret:
            self.stdout.write(self.style.ERROR('⚠ GOOGLE_OAUTH_CLIENT_ID и GOOGLE_OAUTH_SECRET_KEY не установлены в .env'))
            return
        
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
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=secret,
        )
        google_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Google OAuth создан заново (ID={google_app.id})'))
        self.stdout.write(self.style.SUCCESS(f'✅ Привязан к сайту: {site.domain}'))
        
        # Проверка
        total = SocialApp.objects.filter(provider='google').count()
        self.stdout.write(self.style.SUCCESS(f'✅ Всего Google приложений в БД: {total}'))
