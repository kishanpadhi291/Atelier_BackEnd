from django.urls import path, include
from .views import *

urlpatterns = [
    path("notificationcr/", notificationcr.as_view(), name="productcr"),
    path("notificationcrud/<id>", notificationrud.as_view(), name="productrud")
]