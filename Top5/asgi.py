import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Top5 import routing  # Ensure this import matches your project's structure

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Top5.settings')

# Django ASGI application
django_asgi_app = get_asgi_application()

