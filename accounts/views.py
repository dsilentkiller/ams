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

from .serializers import *
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from accounts.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

#to generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
        'refresh':str(refresh), #return refresh token  token for user
        'access': str(refresh.access_token) #return new token
    }

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer =RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Registration Successfully'},status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:           
            return Response({'error_message': str(e)}, 
                                status=status.HTTP_404_NOT_FOUND)




# class TokenObtainPairView():
#     pass


class TokenRefreshView():
    pass
