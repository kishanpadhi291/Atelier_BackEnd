import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .usermanager import CustomUserManager
from cloudinary_storage.storage import MediaCloudinaryStorage

class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class User(AbstractBaseUser,PermissionsMixin):
    username = None
    id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    fullName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phoneNumber=models.CharField(unique=True,max_length=12)
    password = models.CharField(max_length=100)
    profile = models.TextField()
    otp=models.CharField(null=True,blank=True,max_length=12)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phoneNumber"]
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


class Avtar(models.Model):
    image = models.ImageField(upload_to="avtar",blank=True,max_length=1000,storage=MediaCloudinaryStorage())

    def __str__(self):
        return f"{self.image}"