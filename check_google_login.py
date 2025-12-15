import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineTest.settings')
django.setup()

from django.test import Client

client = Client()
response = client.get('/accounts/google/login/')

print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.content)}")
print("\n" + "="*60)
print("ПЕРВЫЕ 500 СИМВОЛОВ ОТВЕТА:")
print("="*60)
print(response.content.decode('utf-8')[:500])
