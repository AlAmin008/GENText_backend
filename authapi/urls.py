from django.urls import path,include
from authapi.views import UserRegistrationView, UserLoginView,UserProfileView,ChangePasswordView,ResetPasswordEmailView, SaveNewPasswordView,ConfirmOTPView, RequestNewOTPView, ResetPasswordEmailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('confirm-otp/',ConfirmOTPView.as_view(),name='confirm-otp'),
    path('request-otp/',RequestNewOTPView.as_view(),name='request-new-otp'),
    path('resetpassword/',ResetPasswordEmailView.as_view(),name='reset-password'),
    path('setnewpassword/<uid>/<token>/',SaveNewPasswordView.as_view(),name='set-new-password'),

]