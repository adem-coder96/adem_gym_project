# gym_project/middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async


class JWTAuthMiddleware:
    """
    Custom middleware that injects the user into the scope if JWT is valid.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # 1. Try to get user from JWT
        # We call the function which handles the internal imports
        scope['user'] = await get_user_from_jwt(scope)

        # 2. If user is anonymous, close the connection immediately
        if scope['user'].is_anonymous:
            await send({
                'type': 'websocket.close',
                'code': 403,  # Forbidden
            })
            return

        # 3. If user is valid, continue to the application
        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))


# HELPER FUNCTION
@database_sync_to_async
def get_user_from_jwt(scope):
    """
    Tries to authenticate a user using the JWT token in the headers.
    Imports are done inside to avoid Django setup errors at startup.
    """
    # Import here to ensure Django is ready
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

    User = get_user_model()

    try:
        # Extract headers from the scope
        headers = dict(scope['headers'])

        # Get the Authorization header string (bytes to string)
        auth_header = headers.get(b'authorization', None)

        if auth_header:
            auth_header = auth_header.decode('utf-8')

            # Verify it starts with 'Bearer '
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

                # Use DRF's JWT Authentication to validate the token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                return user

    except (InvalidToken, TokenError, KeyError):
        pass

    return AnonymousUser()