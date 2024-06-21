from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from app.serializers import SubjectSerializers, StudentSerializer, GroupSerializer,AttendanceSerializer
from rest_framework.exceptions import ValidationError
from app.models import Subject, Student, Group,Attendance
from django.shortcuts import get_object_or_404
from accounts.models import Users
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
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:

            return Response({
                "success": False,
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)

        student.delete()

        return Response({
            "success": True,
            "message": "Student deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

    # ============================= group ================================================

class GroupListAPIView(APIView):
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({
            "success": True,
            "message": "List All Groups",
            "result": serializer.data
        }, status=status.HTTP_200_OK)

class GroupCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                subject_id = request.data.get('subject')
                teacher_id = request.data.get('teacher')
                student_ids = request.data.get('students', [])

                subject = get_object_or_404(Subject, id=subject_id)
                teacher = get_object_or_404(Users, id=teacher_id)

                group, created = Group.objects.get_or_create(
                    subject=subject,
                    teacher=teacher,
                    groupName=request.data.get('groupName'),
                    defaults={
                        'startTime': request.data.get('startTime'),
                        'endTime': request.data.get('endTime'),
                        'active': request.data.get('active', True),  # Set default if not provided
                    }
                )

                # Add students to the group
                if created:
                    group.students.set(student_ids)
                else:
                    group.students.add(*student_ids)

                # Serialize the subject and other related fields
                subject_serializer = SubjectSerializers(group.subject)
                group_data = {
                    "id": group.id,
                    "subject": subject_serializer.data,
                    "teacher": group.teacher.id,
                    "groupName": group.groupName,
                    "students": [student.id for student in group.students.all()],
                    "startTime": group.startTime,
                    "endTime": group.endTime
                }

                if created:
                    message = "Group created successfully."
                    status_code = status.HTTP_201_CREATED
                else:
                    message = "Group already exists."
                    status_code = status.HTTP_200_OK

                return Response({
                    "success": True,
                    "message": message,
                    "result": group_data
                }, status=status_code)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)




class GroupDetailAPIView(APIView):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(group)
        return Response({
            "success": True,
            "message": "Group Detail",
            "result": serializer.data
        }, status=status.HTTP_200_OK)

class GroupUpdateAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid(raise_exception=True):
            subject_id = request.data.get('subject')
            teacher_id = request.data.get('teacher')
            student_ids = request.data.get('students', [])

            subject = get_object_or_404(Subject, id=subject_id)
            teacher = get_object_or_404(Users, id=teacher_id)

            group.subject = subject
            group.teacher = teacher
            group.groupName = request.data.get('groupName')
            group.startTime = request.data.get('startTime')
            group.endTime = request.data.get('endTime')
            group.active = request.data.get('active', group.active)

            group.save()

            # Update students in the group
            group.students.set(student_ids)

            # Serialize the updated data
            subject_serializer = SubjectSerializers(group.subject)
            group_data = {
                "id": group.id,
                "subject": subject_serializer.data,
                "teacher": group.teacher.id,
                "groupName": group.groupName,
                "students": [student.id for student in group.students.all()],
                "startTime": group.startTime,
                "endTime": group.endTime
            }

            return Response({
                "success": True,
                "message": "Successfully updated group",
                "result": group_data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class GroupDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return Response({
            "success": True,
            "message": "Group deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


#======================= Attendance ===============================================
class AttendanceListAPIView(APIView):
    def get(self, request, format=None):
        groups = Attendance.objects.all()
        serializer = AttendanceSerializer(groups, many=True)
        return Response({
            "success": True,
            "message": "List All Groups",
            "result": serializer.data
        }, status=status.HTTP_200_OK)
    
class AttendanceCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                attendance = serializer.save()

                # Serialize the saved attendance record
                attendance_data = {
                    "id": attendance.id,
                    "groupId": attendance.groupId.id,
                    "studentId": attendance.studentId.id,
                    "date": attendance.date,
                    "present": attendance.present,
                }

                return Response({
                    "success": True,
                    "message": "Attendance record created successfully.",
                    "result": attendance_data
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "success": False,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

class AttendanceUpdateAPIView(APIView):

    def put(self, request, pk, format=None):
        attendance = self.get_object(pk)
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Attendance record updated successfully.",
                "result": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response({
            "success": False,
            "message": "Unable to Update attendance record "
        }, status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetailAPIView(APIView):
    def get(self, request, pk):
        group = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(group)
        return Response({
            "success": True,
            "message": "Attendance Detail",
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    
class  AttendanceDeleteAPIView(APIView):
     def delete(self, request, pk, format=None):
        attendance = get_object_or_404(Attendance, pk=pk)
        attendance.delete()
        return Response({
            "success": True,
            "message": "Attendance {attendance.id} deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


