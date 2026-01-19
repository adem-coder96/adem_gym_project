from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_test_notification(request):
    user = request.user  # Send to current user
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",  # Match the consumer group name
        {
            "type": "send_notification",
            "message": "Hello! This is a test notification"
        }
    )
    return JsonResponse({"status": "Notification sent to your account"})