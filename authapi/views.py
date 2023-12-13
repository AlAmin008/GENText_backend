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


def get_new_access_token(refresh_token):
    try:
        refresh_token = RefreshToken(refresh_token)
        new_access_token = str(refresh_token.access_token)
        return new_access_token
    except:
        return None

def sent_mail_to_user(otp,email):
    subject ="GENText Registration OTP"
    message = f"Please Use this OTP to complete your registration process {otp}"
    from_email= settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient)

#generating OTP
def generate_otp(length=6):
    characters = string.digits
    while True:
        otp = ''.join(random.choice(characters) for _ in range(length))
        if otp[0]!= 0:
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
            return Response({"msg":"Please Check Your Email. An OTP is Sent To Confirm Your Registration."},status=status.HTTP_200_OK)
    
class ConfirmOTPView(APIView):
    def post(self,request):
        serializer = ConfirmOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"msg":"User Not Registered"},status=status.HTTP_401_UNAUTHORIZED) 
            OTP = serializer.data.get('OTP')  
            print(type(OTP))
            print((user.OTP_generation_time - datetime.now(timezone.utc)))
            if str(user.OTP) == OTP and ((datetime.now(timezone.utc)-user.OTP_generation_time)<= timedelta(minutes=2)):
                user.is_active = 1
                user.save()
                return Response({"msg":"Registration Successful"},status=status.HTTP_201_CREATED) 
            return Response({"msg":"Incorrect OTP or Expired"},status=status.HTTP_401_UNAUTHORIZED) 

class RequestNewOTPView(APIView):
    def post(self,request):
        serializer = RequestNewOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({"msg":"User Not Registered"},status=status.HTTP_401_UNAUTHORIZED) 
                OTP = generate_otp() 
                user.OTP = OTP
                user.OTP_generation_time = datetime.now()
                user.save()
                return Response({"msg":"A new OTP sent to your email. Please Check!"},status=status.HTTP_200_OK) 
    
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
                return Response({"token":token,"user":{"id":user.id,"fullname":user.name,"email":user.email}},status=status.HTTP_200_OK)
            else:    
                return Response({"errors":"Email or Password is not valid"},status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# from datetime import datetime
# from rest_framework_simplejwt.tokens import AccessToken

# def is_access_token_expired(access_token):
#     """
#     Check if the provided access token has expired.

#     Parameters:
#     - access_token (str): The access token to check.

#     Returns:
#     - bool: True if the token has expired, False otherwise.
#     """
#     try:
#         token = AccessToken(access_token)
#         expiration_time = token.payload.get('exp', 0)
#         current_time = datetime.utcnow().timestamp()
#         return current_time > expiration_time
#     except Exception as e:
#         # Handle exceptions, such as an invalid token format
#         print(f"Error checking token expiration: {str(e)}")
#         return True  # Treat as expired if an error occurs

# Example usage:



# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

    
    
#     def get(self, request):
#         access_token = request.data.get('access_token')
#         if is_access_token_expired(access_token):
#             print("Access token has expired.")
#             refresh_token = request.data.get('refresh_token')
#             refresh_token = RefreshToken(refresh_token)    
#             access_token = str(refresh_token.access_token) 
#             print(access_token)
#         else:
#             print("Access token is still valid.")
        
#         return Response({"msg":"Done"}, status=status.HTTP_200_OK)  
    
        
            



class ChangePasswordView(APIView):
    # renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data,context={'user':request.user})
        print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Changed Successful"},status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        
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
        
        
