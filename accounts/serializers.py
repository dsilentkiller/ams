from rest_framework import serializers
from accounts.models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'fullName', 'email', 'course',
                  'phoneNumber', 'role', 'is_staff', 'is_admin']
