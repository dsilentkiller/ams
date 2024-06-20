from rest_framework import serializers
from app.models import *


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subjectCode', 'subjectName',
                  'numberOfClasses', 'created']


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'fullName', 'email']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'fullName', 'email', 'phoneNumber', 'created']


class GroupSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    students = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'subject', 'students', 'teacher',
                  'groupName', 'startTime', 'endTime']
