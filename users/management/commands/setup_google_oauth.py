from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os


class Command(BaseCommand):
    help = 'Настройка Google OAuth для django-allauth'

    def handle(self, *args, **options):
        # Обновляем Site
        site = Site.objects.get_current()
        if site.domain != '127.0.0.1:8000':
            site.domain = '127.0.0.1:8000'
            site.name = 'OnlineTest'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Site обновлен: {site.domain}'))
        
        # Создаем или обновляем Google Social App
        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('❌ Переменные окружения GOOGLE_OAUTH_CLIENT_ID/GOOGLE_OAUTH_CLIENT_SECRET не заданы'))
            self.stdout.write(self.style.WARNING('Установите их в окружении перед запуском команды.'))
            return

        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            self.stdout.write(self.style.SUCCESS('✓ Google App обновлен'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Google App создан'))
        
        # Привязываем к текущему Site
        if site not in google_app.sites.all():
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f'✓ Google App привязан к {site.domain}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Google OAuth успешно настроен!'))
        self.stdout.write(self.style.WARNING('\nДобавьте в Google Cloud Console:'))
        self.stdout.write(self.style.WARNING('Authorized redirect URI: http://127.0.0.1:8000/accounts/google/login/callback/'))
