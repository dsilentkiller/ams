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
        fields = ['id', 'fullName', 'email', 'course',
                  'phoneNumber', 'role', 'is_staff', 'is_admin']
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
        fields = ('password', 'password', 'confirm_password',
                  'email', 'fullName', 'phoneNumber')
        # extra_kwargs = {
        #   'first_name': {'required': True},
        #   'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            # username=validated_data['username'],
            email=validated_data['email'],
            fullName=validated_data['fullName'],
            phoneNumber=validated_data['phoneNumber'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user
# login serializer


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )
    # password = serializers.CharField(
    #     write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Users
        fields = ('password',
                  'email')
