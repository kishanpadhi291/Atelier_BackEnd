from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path("create/", UserRegistration.as_view(), name="user"),
    path("profile/", UserProfile.as_view(), name="user"),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("avtar/", UserProfile.as_view(), name="avtar"),
    path("list", UsersList.as_view(), name="users_list"),
    path("user/<pk>", UserbyId.as_view(), name="users_By_Id"),
    path("current-user", CurrentUser.as_view(), name="CurrentUser"),
    path("user-issue", UserIssueBasicDetails.as_view(), name="UserIssueBasicDetails"),
    path("change-password", ChangeInformation.as_view(), name="ChangeInformation"),
    path("change-profile", ChangeInformation.as_view(), name="ChangeInformation"),
    path('mobilelogin/token/', MobileLogin.as_view(), name='token_obtain_pair_mobile'),
    path('otpgeneration/', OtpGeneration.as_view(), name='generate_otp'),
    path('otpverification/', OtpVerification.as_view(), name='verify_otp'),
    path('blank_otp/', Blank_otp.as_view(), name='blank_otp'),
]
