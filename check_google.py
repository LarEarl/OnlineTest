from allauth.socialaccount.models import SocialApp

app = SocialApp.objects.get(provider='google')
print(f'App: {app.name}')
print(f'Client ID: {app.client_id}')
print(f'Sites: {[s.domain for s in app.sites.all()]}')
