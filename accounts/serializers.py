from rest_framework import serializers
from accounts.models import Users
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
import logging
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode


from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
logger = logging.getLogger(__name__)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'fullName', 'email',
                  'phoneNumber', 'role', 'is_staff', 'is_admin', 'created_at', 'updated_at']
# register serializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('id', 'password', 'password', 'confirm_password',
                  'email', 'fullName', 'phoneNumber', 'role', 'created_at', 'updated_at')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            email=validated_data['email'],
            fullName=validated_data['fullName'],
            phoneNumber=validated_data['phoneNumber'],
            role=validated_data['role'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# login serializer


class LoginSerializer(serializers.ModelSerializer):
    # email and password taken
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['email', 'password']


#################################### change password ########################
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = Users
        fields = ['old_password',
                  'new_password']
        #

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
 # Include this to fix the AssertionError

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'] = serializers.CharField()


##################################### profile #########################
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'fullName',  'email']

    # to update profile

    # def update(self, instance, validated_data):
    #     instance.fullName = validated_data.get('fullName', instance.fullName)
    #     instance.phoneNumber = validated_data.get(
    #         'phoneNumber', instance.phoneNumber)
    #     instance.role = validated_data.get('role', instance.role)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance

################# forgetpasswordserializer ####################################


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check if the email exists in the User model.
        """
        try:
            self.user = Users.objects.get(email=value)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return value

    def send_password_reset_email(self):
        """
        Send a password reset email using Django's default token generator.
        """
        if hasattr(self, 'user') and self.user is not None:
            context = {
                'user': self.user,
                'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
                'token': default_token_generator.make_token(self.user),
            }
            return context
        else:
            raise serializers.ValidationError("No user found for this email")

# class ForgetPasswordSerializer(serializers.Serializer):
    # email = serializers.EmailField()

    # def validate_email(self, value):
    #     try:
    #         self.user = Users.objects.get(email=value)
    #     except Users.DoesNotExist:
    #         raise serializers.ValidationError(
    #             "User with this email does not exist.")
    #     return value

    # def send_password_reset_email(self):
    #     if hasattr(self, 'user') and self.user is not None:
    #         context = {
    #             'user_id': self.user.id,
    #             'email': self.user.email,
    #             'fullName': self.user.fullName,
    #             'phoneNumber': self.user.phoneNumber,
    #             'role': self.user.role,
    #             'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
    #             'token': default_token_generator.make_token(self.user),
    #         }
    #         # You can implement your email sending logic here
    #         # Example:
    #         # send_mail(subject="Password Reset", template="email/password_reset.html", context=context)
    #         # password_reset_url = f"http://example.com/reset/{uid}/{token}/"
    #         return context
    #     else:
    #         raise serializers.ValidationError("No user found for this email")


######################### sendPasswordresetemail ############
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            self.user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link.")

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError("Invalid reset link.")

        return attrs

    def save(self):
        new_password = self.validated_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        return self.user

# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(
#         write_only=True)

#     uid = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         try:
#             uid = force_text(urlsafe_base64_decode(attrs['uid']))
#             self.user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             raise serializers.ValidationError("Invalid reset link.")

#         if not default_token_generator.check_token(self.user, attrs['token']):
#             raise serializers.ValidationError("Invalid reset link.")

#         return attrs

#     def save(self):
#         new_password = self.validated_data['new_password']
#         self.user.set_password(new_password)
#         self.user.save()
#         return self.user
