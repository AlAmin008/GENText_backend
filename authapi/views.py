from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authapi.serializers import SaveNewPasswordSerializer, UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer, ChangePasswordSerializer, SendResetEmailSerializer, ConfirmOTPSerializer, RequestNewOTPSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authapi.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime,timedelta, timezone

import string, random


def sent_mail_to_user(otp,email):
    subject ="GENText Reistration OTP"
    message = f"Please Use is OTP to complete your registration process {otp}"
    from_email= settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient)

#generating OTP
def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

#generating Manual Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            OTP = generate_otp()
            serializer.validated_data['OTP'] = OTP
            user=serializer.save()
            sent_mail_to_user(OTP,serializer.data.get('email'))
            # token = get_tokens_for_user(user)
            return Response({"msg":"Please Check Your Email. An OTP is Sent To Confirm Your Registration."},status=status.HTTP_201_CREATED)
    
class ConfirmOTPView(APIView):
    def post(self,request):
        serializer = ConfirmOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"msg":"User Not Registered"},status=status.HTTP_404_NOT_FOUND) 
            OTP = serializer.data.get('OTP')  
            print(type(OTP))
            print((user.OTP_generation_time - datetime.now(timezone.utc)))
            if str(user.OTP) == OTP and ((datetime.now(timezone.utc)-user.OTP_generation_time)<= timedelta(minutes=2)):
                user.is_active = 1
                user.save()
                return Response({"msg":"Registration Successful"},status=status.HTTP_201_CREATED) 
            return Response({"msg":"Incorrect OTP or Expired"},status=status.HTTP_404_NOT_FOUND) 
        # return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND) 

class RequestNewOTPView(APIView):
    def post(self,request):
        serializer = RequestNewOTPSerializer(data=request.data)
        if serializer.is_valid():
                email = serializer.data.get('email')
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({"msg":"User Not Registered"},status=status.HTTP_404_NOT_FOUND) 
                OTP = generate_otp() 
                user.OTP = OTP
                user.OTP_generation_time = datetime.now()
                user.save()
                return Response({"msg":"A new OTP sent to your email. Please Check!"},status=status.HTTP_200_OK) 
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)   
    
class UserLoginView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password,is_active=1)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token,"msg":"Login Successful"},status=status.HTTP_200_OK)
            else:    
                return Response({"errors":{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    # renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    # renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data,context={'user':request.user})
        print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Changed Successful"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)
        
class ResetPasswordEmailView(APIView):
    # renderer_classes =[UserRenderer]

    def post(self,request):
        serializer = SendResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset message sent. Please check your email"},status=status.HTTP_201_CREATED)

class SaveNewPasswordView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self,request,uid,token):
        serializer = SaveNewPasswordSerializer(data=request.data,context ={'uid':uid,'token':token}) 
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset Successfully"},status=status.HTTP_201_CREATED)          