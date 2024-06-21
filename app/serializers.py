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

    def create(self, validated_data):
        subject_data = validated_data.pop('subject')
        teacher_data = validated_data.pop('teacher')
        students_data = validated_data.pop('students')

        subject_instance, _ = Subject.objects.get_or_create(**subject_data)
        teacher_instance, _ = Users.objects.get_or_create(**teacher_data)
        students_instances = [Users.objects.get_or_create(
            **student_data)[0] for student_data in students_data]

        group = Group.objects.create(
            subject=subject_instance, teacher=teacher_instance, **validated_data)
        group.students.set(students_instances)
        return group

    def update(self, instance, validated_data):
        subject_data = validated_data.pop('subject', None)
        teacher_data = validated_data.pop('teacher', None)
        students_data = validated_data.pop('students', None)

        if subject_data:
            subject_instance, _ = Subject.objects.get_or_create(**subject_data)
            instance.subject = subject_instance

        if teacher_data:
            teacher_instance, _ = Users.objects.get_or_create(**teacher_data)
            instance.teacher = teacher_instance

        if students_data:
            students_instances = [Users.objects.get_or_create(
                **student_data)[0] for student_data in students_data]
            instance.students.set(students_instances)

        instance.name = validated_data.get('name', instance.name)
        instance.startTime = validated_data.get(
            'startTime', instance.startTime)
        instance.endTime = validated_data.get('endTime', instance.endTime)
        instance.save()
        return instance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model =Attendance
        fields=['id','date','groupId','studentId','present','created']
