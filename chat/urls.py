from django.urls import path
from .views import *

urlpatterns = [
    path("my-messages/<receiver_id>/", MyInbox.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", GetMessages.as_view()),
    path("send-messages/", SendMessages.as_view()),
    path("search/<name>/", SearchUser.as_view())
]
