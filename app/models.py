from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone

# ====================== subject =================================


class Subject(models.Model):
    subjectName = models.CharField(
        max_length=120, null=False, blank=False, help_text="subjectName is required")
    subjectCode = models.CharField(max_length=120,
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
        max_length=120, blank=True, null=True, help_text="fullName field is required")
    email = models.EmailField(unique=True, blank=True,
                              null=True, help_text="email field is required")
    phoneNumber = models.CharField(
        max_length=15, blank=True, null=True, help_text="phoneNumber field is required")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullName}-{self.email}-{self.phoneNumber}"
