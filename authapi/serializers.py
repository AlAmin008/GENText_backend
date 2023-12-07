from django.forms import ValidationError
from rest_framework import serializers
from authapi.models import User
from django.contrib.auth.hashers import check_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings


def sent_mail_to_user(email,subject,message):
    from_email= settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwrgs = {
            'password':{'write_only':True}
        }
    
    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        return data
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
class ConfirmOTPSerializer(serializers.Serializer):
    OTP = serializers.CharField(max_length=6,min_length=6) 
    email = serializers.EmailField(max_length=255)

class RequestNewOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields= ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255, min_length=6, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(max_length=255, min_length=6, write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=255,min_length=6,write_only=True, style={'input_type':'password'})

    class Meta:
        fields = ['current_password', 'new_password','confirm_password']

    def validate(self, attrs):
        user = self.context['user']
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password == confirm_password:
            if not check_password(current_password, user.password):
                raise serializers.ValidationError("Incorrect password!")
            # If the current password is correct, update the user's password
            user.set_password(new_password)
            user.save()
            return attrs
        raise serializers.ValidationError("New passwords doesn't match")

        

class SendResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields =['email']
    
    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link ',link)
            # send email
            subject ="GENText Reset Password Link"
            message = f"Please click the link below to set a new password. {link}"
            sent_mail_to_user(email,subject,message)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')
        
class SaveNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, min_length=6, write_only=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(max_length=255, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        fields = ['current_password', 'new_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        uid = self.context.get('uid')
        token =self.context.get('token')


        if new_password !=new_password2 :
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Token is not Valid or Expired")
        user.set_password(new_password)
        user.save()
        return attrs