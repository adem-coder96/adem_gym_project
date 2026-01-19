import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from gym_project.middleware import JWTAuthMiddlewareStack  # Use your custom middleware
import notifications.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gym_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(  # Use your JWT middleware
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})