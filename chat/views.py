from django.shortcuts import render
from rest_framework import status

from .models import ChatMessage
from user.models import User
from .serializer import MessageSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from user.serializer import UserListSerializer
from rest_framework.views import APIView, Response


# Create your views here.
class MyInbox(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['receiver_id']

        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id) |
                    Q(receiver__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) |
                            Q(receiver=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages


class GetMessages(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        messages = ChatMessage.objects.filter(sender__in=[sender_id, receiver_id],
                                              receiver__in=[sender_id, receiver_id])
        return messages


class SendMessages(CreateAPIView):
    serializer_class = MessageSerializer


class SearchUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        name = self.kwargs['name']
        logged_in_user = self.request.user
        users = User.objects.filter(Q(fullName__icontains=name) | Q(email__icontains=name) & ~Q(id=logged_in_user.id))
        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
