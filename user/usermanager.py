from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email,phoneNumber, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phoneNumber:
            raise ValueError('The PhoneNumber field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,phoneNumber=phoneNumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,phoneNumber,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email,phoneNumber,password, **extra_fields)