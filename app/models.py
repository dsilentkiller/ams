from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from accounts.models import Users
# ====================== subject =================================


class Subject(models.Model):
    subjectName = models.CharField(
        max_length=255, null=False, blank=False, help_text="subjectName is required")
    subjectCode = models.CharField(max_length=255,
                                   unique=True, blank=False, null=False, help_text="subjectCode is required")
    numberOfClasses = models.BigIntegerField(
        blank=False, null=False, help_text="numberOfClasses is required")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subjectName} - {self.subjectCode}"

# ============ student ===================================


class Student(models.Model):
    fullName = models.CharField(
        max_length=255, blank=True, null=True, help_text="fullName field is required")
    email = models.EmailField(unique=True, blank=True,
                              null=True, help_text="email field is required")
    phoneNumber = models.CharField(
        max_length=15, blank=True, null=True, help_text="phoneNumber field is required")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullName}-{self.email}-{self.phoneNumber}"
# ==============================Techer ====================================================


# class Teacher(models.Model):
#     pass

# ================== Group ==================================================================================================================


class Group(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, max_length=200,
                                null=False, blank=False, help_text="subject is required")

    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, max_length=255,
                                null=False, blank=False, help_text="Teacher is Required ")

    groupName = models.CharField(
        null=False, blank=False, max_length=255, unique=True, help_text="groupName is required")
    students = models.OneToOneField(Student, on_delete=models.CASCADE, blank=False,
                                    null=False, help_text="student is required")
    startTime = models.CharField(max_length=255, blank=False, null=False)
    endTime = models.CharField(max_length=255, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}-{self.teacher}-{self.groupName}-{self.students}'
