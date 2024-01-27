from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .models import Notification
from .notificationSerializer import NotificationSerializer
# Create your views here.

class notificationrud(RetrieveUpdateDestroyAPIView):
    queryset=Notification.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = NotificationSerializer

class notificationcr(ListCreateAPIView):
    queryset=Notification.objects.all()
    serializer_class = NotificationSerializer