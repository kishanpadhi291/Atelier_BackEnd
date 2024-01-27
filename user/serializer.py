from rest_framework import serializers
from .models import *


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","fullName","profile","email","phoneNumber","is_staff"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","fullName","email","profile","phoneNumber","is_staff"]

class ProfileAvtarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avtar
        fields = "__all__"
