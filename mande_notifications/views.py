from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import Customer, Worker

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        data = request.data

        try:
            user_id = int(data['user'])
        except Exception:
            return Response(status=400)
        
        try:
            as_customer = data['as_customer'].lower() == 'true'
        except Exception:
            as_customer = False

        if (as_customer):
            if (not Customer.objects.filter(user__id=user_id).exists()):
                return Response(status=400)
            else:
                response = super().create(request, *args, **kwargs)
                return response
        else:
            if (not Worker.objects.filter(user__id=user_id).exists()):
                return Response(status=400)
            else:
                response = super().create(request, *args, **kwargs)
                return response



    def list_filter_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user', None)

        if user_id:
            filtered_notifications = Notification.objects.filter(user__id=user_id)
            serializer = NotificationSerializer(filtered_notifications, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)
