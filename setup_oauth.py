import os
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineTest.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get credentials from environment
client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
secret = os.getenv('GOOGLE_OAUTH_SECRET_KEY', '')

if not client_id or not secret:
    print('⚠ GOOGLE_OAUTH_CLIENT_ID и GOOGLE_OAUTH_SECRET_KEY не установлены в .env')
    exit(1)

# Проверяем текущий Site
site = Site.objects.get_current()
print(f"Текущий Site: {site.domain}")

# Удаляем ВСЕ старые Google apps
google_apps = SocialApp.objects.filter(provider='google')
if google_apps.exists():
    count = google_apps.count()
    google_apps.delete()
    print(f"❌ Удалено {count} старых Google приложений")

# Создаем НОВОЕ приложение с данными из .env
google_app = SocialApp.objects.create(
    provider='google',
    name='Google OAuth',
    client_id=client_id,
    secret=secret
)
google_app.sites.add(site)

print(f"✅ Новое Google OAuth создано!")
print(f"   Client ID: {google_app.client_id[:30]}...")
print(f"   Привязано к Site: {site.domain}")
print(f"\n🔗 Перейди на http://127.0.0.1:8000/users/login/ и кликни на кнопку Google")
