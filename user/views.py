import json
import random
from django.core.mail import send_mail
import requests
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework import generics
from user.serializer import UserListSerializer, ProfileAvtarSerializer, UserProfileSerializer
from user.models import User, Avtar
from issue.issueSerializer import GroupViseIssueSerializer
from .utils import *
from django.conf import settings


class OtpGeneration(APIView):
    def post(self, request):
        otp = generateotp()
        subject = 'Otp Verification Atelier'
        body = f'Otp to create a temporary password:- {otp}'
        if User.objects.filter(Q(email=request.data['identifier']) | Q(phoneNumber=request.data['identifier'])).exists():
            user = User.objects.filter(Q(email=request.data['identifier']) | Q(phoneNumber=request.data['identifier']))[0]
            user.otp = otp
            user.save()
            print(user.fullName,body)
            # send_mail(
            #     subject,
            #     body,
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            # )
            return Response({'detail': 'otp generated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No active account with the given Email'},
                            status=status.HTTP_400_BAD_REQUEST)


class Blank_otp(APIView):
    def post(self,request):
        user = User.objects.filter(Q(email=request.data['identifier']) | Q(phoneNumber=request.data['identifier']))[0]
        user.otp = None
        user.save()
        return Response(status=status.HTTP_200_OK)

class OtpVerification(APIView):
    def post(self, request):
        if User.objects.filter(Q(email=request.data['identifier']) | Q(phoneNumber=request.data['identifier'])).exists():
            user = User.objects.filter(Q(email=request.data['identifier']) | Q(phoneNumber=request.data['identifier']))[0]
            if user.otp == request.data['otp']:
                password = generatepassword()
                print(password)
                user.set_password(password)
                user.save()
                print(user.check_password(password))
                print(user.fullName)
                print('verified')
                return Response({'detail': 'otp verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Incorrect otp'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No active account with the given Email'},
                            status=status.HTTP_400_BAD_REQUEST)

class MobileLogin(APIView):
    def post(self, request):
        try:
            req = request.data
            mobile = req['mobile']
            password = req['password']
            user = User.objects.get(phoneNumber=mobile)
            email = user.email
            url = 'http://127.0.0.1:8000/user/login/token/'
            data = {'email': email, 'password': password}
            headers = {
                'Content-Type': 'application/json',
            }
            json_data = json.dumps(data)
            response = requests.post(url=url, data=json_data, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No active user with given credential"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    def post(self, request):
        user = User()
        user.email = request.data["email"]
        user.phoneNumber = request.data['phoneNumber']
        user.profile = request.data["profile"]
        user.fullName = request.data["fullName"]
        try:
            user.set_password(request.data["password"])
            user.save()
            return Response({"success": "Account created successfully"})
        except Exception:
            return Response({"error": "Something Went Wrong"})


class UserProfile(generics.ListCreateAPIView):
    queryset = Avtar.objects.all()
    serializer_class = ProfileAvtarSerializer


class UsersList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserListSerializer

class UserbyId(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

    def get_queryset(self):
        pk=self.kwargs['pk']
        user=User.objects.filter(pk=pk)
        return user

class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserProfileSerializer(User.objects.get(email=request.user))
        return Response({"currentUser": user.data}, status=status.HTTP_200_OK)


class UserIssueBasicDetails(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(email=request.user)
        serializer = GroupViseIssueSerializer(user)
        return Response(serializer.data)


class ChangeInformation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(email=request.user)
        if user.check_password(request.data["currentPassword"]):
            user.set_password(request.data["newPassword"])
            user.save()
            return Response({"success": "Password Changed Successfully"})
        else:
            return Response({"error": "Invalid Password"})

    def patch(self, request):
        user = User.objects.get(email=request.user)
        user.profile = request.data["profile"]
        user.save()
        return Response({"success", user}, status=status.HTTP_200_OK)
