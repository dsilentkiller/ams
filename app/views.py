from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from app.serializers import SubjectSerializers
from rest_framework.exceptions import ValidationError


class SubjectAPIView(APIView):
    def post(self, request, **args):
        serializer = SubjectSerializers
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
