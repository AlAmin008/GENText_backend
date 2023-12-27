from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authapi.serializers import SaveNewPasswordSerializer, UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer, ChangePasswordSerializer, SendResetEmailSerializer, ConfirmOTPSerializer, EmailSerializer,NameSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authapi.models import User
from django.conf import settings
from datetime import datetime,timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
import string, random
from rest_framework.parsers import MultiPartParser
import os


# def get_new_access_token(refresh_token):
#     try:
#         refresh_token = RefreshToken(refresh_token)
#         new_access_token = str(refresh_token.access_token)
#         return new_access_token
#     except:
#         return None

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

def generate_otp(length=6):
    characters = string.digits
    while True:
        otp = ''.join(random.choice(characters) for _ in range(length))
        if otp[0]!= '0':
            return otp

def is_image(file_obj):
    image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp']
    extension=file_obj.name.lower().split(".")[-1]
    return extension in image_extensions

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
            sent_mail_to_user(OTP,serializer.data.get('email'),user.name)
            return Response({"message":"Please Check Your Email. An OTP is Sent To Confirm Your Registration."},status=status.HTTP_200_OK)
    
class ConfirmOTPView(APIView):
    def post(self,request):
        serializer = ConfirmOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error":"User Not Registered"},status=status.HTTP_401_UNAUTHORIZED) 
            OTP = serializer.data.get('OTP')  
            print(type(OTP))
            print((user.OTP_generation_time - datetime.now(timezone.utc)))
            if str(user.OTP) == OTP and ((datetime.now(timezone.utc)-user.OTP_generation_time)<= timedelta(minutes=2)):
                user.is_active = 1
                user.save()
                return Response({"message":"Registration Successful"},status=status.HTTP_201_CREATED) 
            return Response({"error":"Incorrect OTP or Expired"},status=status.HTTP_401_UNAUTHORIZED) 

class RequestNewOTPView(APIView):
    def post(self,request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({"error":"User Not Registered"},status=status.HTTP_401_UNAUTHORIZED) 
                OTP = generate_otp() 
                user.OTP = OTP
                user.OTP_generation_time = datetime.now()
                user.save()
                sent_mail_to_user(OTP,email,user.name)
                return Response({"message":"A new OTP sent to your email. Please Check!"},status=status.HTTP_200_OK) 

class CancleRegistrationView(APIView):
    def post(self,request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            try:
                user = User.objects.get(email=email,is_active=0)
                user.delete()
            except User.DoesNotExist:
                return Response({"error":"User Not Registered or Account Already Activated!"},status=status.HTTP_401_UNAUTHORIZED) 
            return Response({"message":"User Info Successfully Deleted"},status=status.HTTP_200_OK) 

class UserLoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            login_id = serializer.data.get('login_id')
            password = serializer.data.get('password')
            if '@' in login_id:
                user = User.objects.get(email=login_id)
                login_id = user.login_id 
            user = authenticate(login_id=login_id,password=password,is_active=1)
            if user is not None:
                token = get_tokens_for_user(user)
                user.last_login = datetime.now()
                user.save()
                return Response({"token":token,"user":{"id":user.id,"fullname":user.name,"email":user.email,"api_token":token['access'],"is_admin": user.is_admin,"UserId":user.login_id}},status=status.HTTP_200_OK)
            else:    
                return Response({"error":"Email or Password is not valid"},status=status.HTTP_401_UNAUTHORIZED)

class GetUserByTokenView(APIView):

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"id":user.id,"fullname":user.name,"email":user.email,"UserId":user.login_id}, status=status.HTTP_200_OK)

# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"message":"Password Changed Successful"},status=status.HTTP_201_CREATED)
        
class ResetPasswordEmailView(APIView):

    def post(self,request):
        serializer = SendResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message":"Password Reset message sent. Please check your email"},status=status.HTTP_201_CREATED)

class SaveNewPasswordView(APIView):

    def post(self,request,uid,token):
        serializer = SaveNewPasswordSerializer(data=request.data,context ={'uid':uid,'token':token}) 
        if serializer.is_valid(raise_exception=True):
            return Response({"message":"Password Reset Successfully"},status=status.HTTP_201_CREATED)    

class ResetNameView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,uid):
        serializer =  NameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(id=uid,is_active=1)
                new_name = serializer.data.get('new_name')
                user.name= new_name
                user.save()
                return Response({"message":"Name Successfully Changed"},status=status.HTTP_200_OK)    
            except User.DoesNotExist:
                return Response({"error":"User Doesn't Exist"},status=status.HTTP_401_UNAUTHORIZED) 
               
class SetLoginIDView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request,uid):
        serializer = NameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(id=uid,is_active=1)
                new_name = serializer.data.get('new_name')
                if '@' in new_name:
                    return Response({"error":"This Login Id is not Acceptable"},status=status.HTTP_403_FORBIDDEN)    
                try:
                    user = User.objects.get(login_id=new_name)
                    return Response({"error":"This Login Id Already Exist"},status=status.HTTP_403_FORBIDDEN)    
                except user.DoesNotExist:
                    user.login_id= new_name
                    user.save()
                    return Response({"message":"Login Id Successfully Changed"},status=status.HTTP_200_OK)    
            except User.DoesNotExist:
                return Response({"error":"User Doesn't Exist"},status=status.HTTP_401_UNAUTHORIZED) 

class UploadImageView(APIView):

    parser_classes = (MultiPartParser,)
    permission_classes=[IsAuthenticated]

    def post(self, request,uid, *args, **kwargs):
        file_obj = request.FILES.get('image')
        if file_obj:
            if is_image(file_obj):
                user = User.objects.get(id=uid)
                folder_path = os.path.join(settings.BASE_DIR, f"media\{user.name}\{file_obj.name}")
                # Ensure the folder exists, create it if necessary
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path,file_obj.name)
                with open(file_path, 'wb') as destination_file:
                    for chunk in file_obj.chunks():
                        destination_file.write(chunk)
                return Response({'message': 'Image Successfully Uploaded'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Only Image is Acceptable'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'file doesn\'t exist'}, status=status.HTTP_204_NO_CONTENT)
        
 
