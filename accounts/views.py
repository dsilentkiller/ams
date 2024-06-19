
from django.http import HttpRequest
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin
)
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from accounts.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string

from django.utils.encoding import force_str
User = get_user_model()


def get_tokens_for_user(user):
    # Define expiration times
    access_token_lifetime = timedelta(minutes=15)
    refresh_token_lifetime = timedelta(days=7)

    # Get current UTC time
    current_utc_time = datetime.now(timezone.utc)

    # Generate tokens with expiration and security key
    refresh = RefreshToken.for_user(user)
    # Add security key to refresh token payload
    refresh_payload = {
        # Convert token to string for JSON serialization
        'token': str(refresh),
        # Convert expiration to Unix timestamp
        'exp': int((current_utc_time + refresh_token_lifetime).timestamp()),
        # Convert security key to string if necessary
        # 'security': str(settings.SECRET_KEY),
        # 'iss': 'your_issuer_name',
        'user_id': str(user.id),
    }

    access = AccessToken.for_user(user)
    # Add security key to access token payload
    access_payload = {
        'token': str(access),  # Convert token to string for JSON serialization
        # Convert expiration to Unix timestamp
        'exp': int((current_utc_time + access_token_lifetime).timestamp()),
        # Convert security key to string if necessary
        # 'security': str(settings.SECRET_KEY),
        # 'iss': 'your_issuer_name',
        'user_id': str(user.id),
    }

    return {
        'refresh': refresh_payload,
        'access': access_payload,
    }


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user_data = {
                    "id": user.id,
                    "fullName": user.fullName,
                    "email": user.email,
                    "phoneNumber": user.phoneNumber,
                    "role": user.role,
                    "is_active": user.is_active,
                    "is_staff": user.is_staff
                }
                return Response({
                    "success": True,
                    "message": "Successfully authenticated",
                    "result": user_data
                }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,

            }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data.get('email')

                password = serializer.validated_data.get('password')
                user = authenticate(
                    request=request, username=email, password=password)  # always for login and logout view

                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response({
                        "success": True,
                        "message": "Successfully authenticated",
                        'token': token,
                        "result": {
                            "id": user.id,
                            "email": user.email,
                        }}, status=status.HTTP_200_OK)
                    # Redirect to profile page after successful login
                    # return redirect('profile')
                    # status=status.HTTP_200_OK)
                else:
                    return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}},
                                    status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]  # use a List, Not dictionary

    def get(self, request, format=None):
        serializer = ProfileSerializer(
            request.user)  # user request.user to get user
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SendPasswordResetEmailAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             serializer = SendPasswordResetEmailSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 return Response({
#                     "success": True,
#                     "message": f'Password reset link sent. Please change your password Thank you for registering with us. Your default password is: {password}'
#                     # "result": {
#                     #     "id": id,
#                     #     "email": email,
#                     # }
#                 }, status=status.HTTP_200_OK)
#         except ValidationError as e:
#             return Response({
#                 "success": False,
#                 "message": serializer.errors,
#             }, status=status.HTTP_400_BAD_REQUEST)

#################### change password view############################################


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()

            # Update session
            update_session_auth_hash(request, user)

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================== forget password =====================================================
class ForgetPasswordAPIView(APIView):
    def post(self, request, format=None):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.user
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = get_tokens_for_user(user)
                reset_password_url = f"http://frontend-url/reset-password?uid={uid}&token={token}"

                # Send the password reset link to the user's email
                send_mail(
                    'Password Reset Request',
                    f'You can reset your password by clicking the link below:\n{reset_password_url}',
                    'paaruinfo@gmail.com',  # Replace with your email
                    [serializer.validated_data['email']],
                    fail_silently=False,
                )

                return Response({
                    "success": True,
                    "message": "Password reset link sent successfully.",
                    "reset_password_url": reset_password_url,
                }, status=status.HTTP_200_OK)

            except Users.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User with this email does not exist.",
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": False,
            "message": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

############ reset password################################################


class ResetPasswordAPIView(APIView):
    def post(self, request, format=None):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            token = request.data.get('token')

            if token:
                try:
                    user = get_tokens_for_user(user)

                    if user is not None:
                        new_password = serializer.validated_data['password']
                        user.set_password(new_password)
                        user.save()

                        return Response({
                            "success": True,
                            "message": "Password reset successfully."
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "success": False,
                            "message": "Token is invalid or expired."
                        }, status=status.HTTP_400_BAD_REQUEST)
                except (TypeError, ValueError, OverflowError):
                    return Response({
                        "success": False,
                        "message": "Invalid token format."
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "message": "Token is required in request data."
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###### to send new password to user email ################################
