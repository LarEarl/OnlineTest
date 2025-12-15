import os
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineTest.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.urls import reverse

# Проверяем Google app
google_app = SocialApp.objects.filter(provider='google').first()
if not google_app:
    print("❌ Google OAuth не найден в БД!")
    exit(1)

site = Site.objects.get_current()

print("=" * 60)
print("ДИАГНОСТИКА GOOGLE OAUTH")
print("=" * 60)

print(f"\n✓ Site: {site.domain} (ID={site.id})")
print(f"✓ Google App ID: {google_app.id}")
print(f"✓ Provider: {google_app.provider}")
print(f"✓ Client ID: {google_app.client_id[:40]}...")
print(f"✓ Привязано к сайтам: {list(google_app.sites.all())}")

# Проверяем Settings
from django.conf import settings

print(f"\n✓ AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
print(f"✓ SITE_ID: {settings.SITE_ID}")

# Проверяем SOCIALACCOUNT_PROVIDERS
if 'SOCIALACCOUNT_PROVIDERS' in dir(settings):
    providers = settings.SOCIALACCOUNT_PROVIDERS
    if 'google' in providers:
        print(f"✓ Google в SOCIALACCOUNT_PROVIDERS: {providers['google']}")
    else:
        print("❌ Google НЕ в SOCIALACCOUNT_PROVIDERS!")
else:
    print("❌ SOCIALACCOUNT_PROVIDERS не найден в settings!")

print(f"✓ SOCIALACCOUNT_AUTO_SIGNUP: {settings.SOCIALACCOUNT_AUTO_SIGNUP}")
print(f"✓ SOCIALACCOUNT_EMAIL_VERIFICATION: {settings.SOCIALACCOUNT_EMAIL_VERIFICATION}")

print("\n" + "=" * 60)
print("Всё готово! Попробуй кликнуть на Google на странице логина.")
print("=" * 60)
