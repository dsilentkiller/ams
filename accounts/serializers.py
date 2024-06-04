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
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = Users
        fields = ( 'password','new_password','confirm_new_password',
                  'email', 'fullName', 'phoneNumber')
        # extra_kwargs = {
        #   'first_name': {'required': True},
        #   'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            # username=validated_data['username'],
            email=validated_data['email'],
            fullName=validated_data['fullName'],
            phoneNumber=validated_data['phoneNumber'],

        )
        user.set_password(validated_data['new_password'])
        user.save()
        return user
