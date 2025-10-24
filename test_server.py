import os
import django
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating_project.settings')
django.setup()

from django.test import Client

client = Client()
response = client.get('/')
print(f"Status: {response.status_code}")
print(f"Content: {response.content[:100]}...")