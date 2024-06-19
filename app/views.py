from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from app.serializers import SubjectSerializers, StudentSerializer
from rest_framework.exceptions import ValidationError
from app.models import Subject, Student
from django.shortcuts import get_object_or_404

# ====================subject========================================

# crud=>create read update delete


class SubjectListAPIView(APIView):
    '''LIST ALL SUBJECTS LIST'''

    def get(self, request, format=None):
        subjects = Subject.objects.all()  # listing all subjects
        serializers = SubjectSerializers(subjects, many=True)
        return Response({
            "success": True,
            "message": "List All Subjects List",
            "result": serializers.data
        }, status=status.HTTP_201_CREATED)


class SubjectCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = SubjectSerializers(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                subject = serializer.save()
                subject_data = {
                    "id": subject.id,
                    "subjectCode": subject.subjectCode,
                    "subjectName": subject.subjectName,
                    "numberOfClasses": subject.numberOfClasses,
                    "created": subject.created,

                }
                return Response({
                    "success": True,
                    "message": "Successfully Subject Created",
                    "result": subject_data
                }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,

            }, status=status.HTTP_400_BAD_REQUEST)


class SubjectDetailAPIView(APIView):
    def get(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializers(subject)
        return Response(serializer.data)


class SubjectUpdateAPIView(APIView):
    def put(self, request, pk, format=None):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({
                "success": False,
                "message": "Subject not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SubjectSerializers(subject, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            subject_data = {
                "id": subject.id,
                "subjectCode": subject.subjectCode,
                "subjectName": subject.subjectName,
                "numberOfClasses": subject.numberOfClasses,
                "created": subject.created,

            }
            return Response({
                "success": True,
                "message": "Successfully Subject updated ",
                "result": subject_data
            }, status=status.HTTP_200_OK)


class SubjectDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):

        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:

            return Response({
                "success": False,
                "message": "Subject not found."
            }, status=status.HTTP_404_NOT_FOUND)

        subject.delete()

        return Response({
            "success": True,
            "message": "Subject deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# ======================== Student =================================================================================


class StudentListAPIView(APIView):
    model = Student

    def get(self, request, format=None):
        subjects = Student.objects.all()  # listing all subjects
        serializers = StudentSerializer(subjects, many=True)
        return Response({
            "success": True,
            "message": "List All Student List ",
            "result": serializers.data
        }, status=status.HTTP_201_CREATED)


class StudentCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                student = serializer.save()
                student_data = {
                    "id": student.id,
                    "fullName": student.fullName,
                    "email": student.email,
                    "phoneNumber": student.phoneNumber,
                    "created": student.created,

                }
                return Response({
                    "success": True,
                    "message": " Student Created Successfully",
                    "result": student_data
                }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,

            }, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailAPIView(APIView):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(
            {
                "success": True,
                "message": " Student Detail ",
                "result": serializer.data
            }, status=status.HTTP_200_OK)


class StudentUpdateAPIView(APIView):
    def put(self, request, pk, format=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({
                "success": False,
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            student_data = {
                "id": student.id,
                "fullName": student.fullName,
                "email": student.email,
                "phoneNumber": student.phoneNumber,
                "created": student.created,

            }
            return Response({
                "success": True,
                "message": "Successfully Student updated ",
                "result": student_data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": serializer.errors,

        }, status=status.HTTP_400_BAD_REQUEST)


class StudentDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):

        try:
            subject = Student.objects.get(pk=pk)
        except Student.DoesNotExist:

            return Response({
                "success": False,
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)

        subject.delete()

        return Response({
            "success": True,
            "message": "Student deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

    # =============================
