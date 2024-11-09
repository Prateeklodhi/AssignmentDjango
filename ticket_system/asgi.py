"""
ASGI config for ticket_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from ticket.consumers import TicketConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_system.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/tickets/", TicketConsumer.as_asgi()),
        ])
    ),
})
