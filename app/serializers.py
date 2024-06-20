from rest_framework import serializers
from app.models import *


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subjectCode', 'subjectName',
                  'numberOfClasses', 'created']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'fullName', 'email', 'phoneNumber', 'created']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'subject', 'students', 'teacher',
                  'groupName', 'startTime', 'endTime']
