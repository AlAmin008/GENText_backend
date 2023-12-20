from django.urls import path
from authapi.views import UserRegistrationView, UserLoginView,UserProfileView,ChangePasswordView,ResetPasswordEmailView, SaveNewPasswordView,ConfirmOTPView, RequestNewOTPView, ResetPasswordEmailView, GetUserByTokenView, CancleRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('cancel-registration/', CancleRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('change-password/',ChangePasswordView.as_view(),name='changepassword'),
    path('confirm-otp/',ConfirmOTPView.as_view(),name='confirm-otp'),
    path('request-otp/',RequestNewOTPView.as_view(),name='request-new-otp'),
    path('reset-password/',ResetPasswordEmailView.as_view(),name='reset-password'),
    path('set-new-password/<uid>/<token>/',SaveNewPasswordView.as_view(),name='set-new-password'),
    path('get-user-by-token', GetUserByTokenView.as_view(),name='get-user-by-token')
]