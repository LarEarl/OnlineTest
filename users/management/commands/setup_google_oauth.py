from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


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
        # ВАЖНО: Замените YOUR_CLIENT_ID и YOUR_CLIENT_SECRET на реальные значения
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': 'YOUR_CLIENT_ID',  # Укажите свой Client ID из Google Cloud Console
                'secret': 'YOUR_CLIENT_SECRET',  # Укажите свой Client Secret
            }
        )
        
        if not created:
            google_app.client_id = 'YOUR_CLIENT_ID'
            google_app.secret = 'YOUR_CLIENT_SECRET'
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
