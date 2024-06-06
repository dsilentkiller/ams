from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from accounts.serializers import RegisterSerializer

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from accounts.serializers import *
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from django.shortcuts import redirect


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
        'iss': 'your_issuer_name',
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
        'iss': 'your_issuer_name',
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


class SendPasswordResetEmailAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = SendPasswordResetEmailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({
                    "success": True,
                    "message": f'Password reset link sent. Please change your password Thank you for registering with us. Your default password is: {password}'
                    # "result": {
                    #     "id": id,
                    #     "email": email,
                    # }
                }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

# profile


# class ProfileAPIView(APIView):
#     def get(self, request, format=None):
#         user = request.user  # only authenticate user
#         serializer = ProfileSerializer(user)
#         return Response({
#             "success": True,
    #         "message": "Profile Retrived Successfully",
    #         "result": serializer.data

    #     })

    # def post(self, request, format=None):
    #     try:
    #         serializer = ProfileSerializer(data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             email = serializer.validated_data.get('email')
    #             # password = serializer.validated_data.get('password')
    #             fullName = serializer.validated_data.get('fullName')
    #             role = serializer.validated_data.get('role')

    #             return Response({
    #                 "success": True,
    #                 "message": f"profile",
    #                 "fullName": fullName,
    #                 "role": role,
    #                 "email": email,
    #             }, status=status.HTTP_200_OK)

    #     except ValidationError as e:
    #         return Response({
    #             "success": False,
    #             "message": serializer.errors,

    #         }, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Get the authenticated user
        serializer = ProfileSerializer(user)  # Pass the user instance
        return Response({
            "success": True,
            "message": "Profile Retrieved Successfully",
            "result": serializer.data
        })

    def post(self, request, format=None):
        try:
            serializer = ProfileSerializer(
                instance=request.user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Profile updated successfully",
                    "result": serializer.data
                }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
