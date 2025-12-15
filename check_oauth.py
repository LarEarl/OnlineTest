import os
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineTest.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Проверяем текущий Site
site = Site.objects.get_current()
print(f"Текущий Site: {site.domain} (ID={site.id})")

# Проверяем Google apps
google_apps = SocialApp.objects.filter(provider='google')
print(f"\nGoogle Apps в БД: {google_apps.count()}")

if google_apps.count() == 0:
    print("❌ Google OAuth не настроен!")
    print("Создаю новое приложение...")
    
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google OAuth',
        client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID', ''),
        secret=os.getenv('GOOGLE_OAUTH_SECRET_KEY', '')
    )
    google_app.sites.add(site)
    print(f"✅ Google OAuth создан! (ID={google_app.id})")
else:
    for app in google_apps:
        print(f"  - ID: {app.id}, Client ID: {app.client_id[:30]}...")
        print(f"    Sites: {list(app.sites.all())}")
        print(f"    Привязан к текущему Site: {site in app.sites.all()}")
        
        # Если не привязан, привяжем
        if site not in app.sites.all():
            print(f"    ⚠️ Привязываю к Site {site.domain}...")
            app.sites.add(site)
            print(f"    ✅ Привязано!")

print("\n✅ Google OAuth готов к работе!")
