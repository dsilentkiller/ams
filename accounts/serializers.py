from rest_framework import serializers
from accounts.models import Users
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


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
    #email and password taken
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True)
#validate user email and passsword is register or not
    def validate(self,data):
        email =data.get('email')
        password = data.get('password')

        if email and password:
            user =authenticate(request=self.context.get('request'),username=email,password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            else:

                raise serializers.ValidationError('  "Must include "email" and "password" ')
        return data
