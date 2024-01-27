from user.serializer import UserListSerializer
from rest_framework import serializers
from .models import ChatMessage
class MessageSerializer(serializers.ModelSerializer):
    receiver_profile = UserListSerializer(many=False,read_only=True)
    sender_profile = UserListSerializer(many=False,read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver','sender_profile','receiver_profile', 'message', 'date']

    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2