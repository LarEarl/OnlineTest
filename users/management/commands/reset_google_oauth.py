from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


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
        # ВАЖНО: Замените YOUR_CLIENT_ID и YOUR_CLIENT_SECRET на реальные значения
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id='YOUR_CLIENT_ID',  # Укажите свой Client ID из Google Cloud Console
            secret='YOUR_CLIENT_SECRET',  # Укажите свой Client Secret
        )
        google_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Google OAuth создан заново (ID={google_app.id})'))
        self.stdout.write(self.style.SUCCESS(f'✅ Привязан к сайту: {site.domain}'))
        
        # Проверка
        total = SocialApp.objects.filter(provider='google').count()
        self.stdout.write(self.style.SUCCESS(f'✅ Всего Google приложений в БД: {total}'))
