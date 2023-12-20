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
from django.core.mail import EmailMultiAlternatives

import string, random


def get_new_access_token(refresh_token):
    try:
        refresh_token = RefreshToken(refresh_token)
        new_access_token = str(refresh_token.access_token)
        return new_access_token
    except:
        return None

def sent_mail_to_user(otp,email,name):
    subject ="GENText Registration OTP"
    message = f"""<!DOCTYPE html> <html lang='en'><head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Blue and White Card</title>
</head>
<body>
  <table style='width: 100%; max-width: 600px; background-color: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);'>
    <tr>
      <td style='padding: 20px; line-height: 1.6; height: 300px; color: #000;'>
        <!-- Blue-colored card-like div -->
        <p style='margin-bottom: 0; text-align: center; margin-top: -2em'><img src='https://i.postimg.cc/HjDrbfzM/logo.png' alt='Logo' style='display: block; max-width: 55%; margin: auto;'></p>
        <p style='text-align: center; color: black;'>Hello, <b>{name}</b></p>
        <p style='margin-top: 5px;text-align: center; color: black'>Thank you for creating a new account.<br> Here is your 6-digit verification code.</p>
        <p style='margin-top: 5px; font-size: 24px; font-weight: bold; line-height: 1; vertical-align: middle; text-align: center;'>{otp}</p>
      </td>
    </tr>
  </table>
</body>
</html>"""
    from_email= settings.EMAIL_HOST_USER
    recipient = [email]
    email_message = EmailMultiAlternatives(subject,message, from_email, recipient)
    email_message.attach_alternative(message, "text/html") 
    email_message.send()

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
    access_token_exp = refresh.access_token.payload['exp']

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'access_token_exp': access_token_exp
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
                sent_mail_to_user(OTP,email,user.name)
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
                return Response({"token":token,"user":{"id":user.id,"fullname":user.name,"email":user.email,"api_token":token['access'],"refresh":token['refresh'],"access_token_exp":token['access_token_exp']}},status=status.HTTP_200_OK)
            else:    
                return Response({"errors":"Email or Password is not valid"},status=status.HTTP_401_UNAUTHORIZED)

class GetUserByTokenView(APIView):

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({"id":user.id,"fullname":user.name,"email":user.email}, status=status.HTTP_200_OK)

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
        
        
