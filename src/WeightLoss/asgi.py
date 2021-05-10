"""
ASGI config for WeightLoss project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

import channels.asgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeightLoss.settings')

application = get_asgi_application()

channel_layer = channels.asgi.get_channel_layer()
