import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

load_dotenv()


class Command(BaseCommand):
    help = 'Настройка Google OAuth для django-allauth'

    def handle(self, *args, **options):
        # Get credentials from environment
        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
        secret = os.getenv('GOOGLE_OAUTH_SECRET_KEY', '')
        
        if not client_id or not secret:
            self.stdout.write(self.style.ERROR('⚠ GOOGLE_OAUTH_CLIENT_ID и GOOGLE_OAUTH_SECRET_KEY не установлены в .env'))
            return
        
        # Обновляем Site
        site = Site.objects.get_current()
        if site.domain != '127.0.0.1:8000':
            site.domain = '127.0.0.1:8000'
            site.name = 'OnlineTest'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Site обновлен: {site.domain}'))
        
        # Создаем или обновляем Google Social App
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = secret
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
