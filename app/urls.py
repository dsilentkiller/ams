from django.urls import path, include
from app import views

urlpatterns = [
    # ============ SUBJECT ================================================================
    path('subject/new/', views.SubjectCreateAPIView.as_view(), name="subject_create"),
    path('subject/list/', views.SubjectListAPIView.as_view(), name="subject_list"),
    path('subject/detail/<int:pk>/',
         views.SubjectDetailAPIView.as_view(), name="subject_detail"),
    path('subject/update/<int:pk>/',
         views.SubjectUpdateAPIView.as_view(), name="subject_update"),
    path('subject/delete/<int:pk>/',
         views.SubjectDeleteAPIView.as_view(), name="subject_delete"),
    # ============================================ Student ========================
    path('student/new/', views.StudentCreateAPIView.as_view(), name="student_create"),
    path('student/list/', views.StudentListAPIView.as_view(), name="student_list"),
    path('student/detail/<int:pk>/',
         views.StudentDetailAPIView.as_view(), name="student_detail"),
    path('student/update/<int:pk>/',
         views.StudentUpdateAPIView.as_view(), name="student_update"),
    path('student/delete/<int:pk>/',
         views.StudentDeleteAPIView.as_view(), name="student_delete"),
    # =============================================== Group=======================================
    path('group/new/', views.GroupCreateAPIView.as_view(), name="group_create"),
    path('group/list/', views.GroupListAPIView.as_view(), name="group_list"),
    path('group/detail/<int:pk>/',
         views.GroupDetailAPIView.as_view(), name="group_detail"),
    path('group/update/<int:pk>/',
         views.GroupUpdateAPIView.as_view(), name="group_update"),
    path('group/delete/<int:pk>/',
         views.GroupDeleteAPIView.as_view(), name="group_delete"),

#=================== Attendance ===============================================================
  path('attendance/new/', views.AttendanceCreateAPIView.as_view(), name="attendance_create"),
    path('attendance/list/', views.AttendanceListAPIView.as_view(), name="attendance_list"),
    path('attendance/detail/<int:pk>/',
         views.AttendanceDetailAPIView.as_view(), name="attendance_detail"),
    path('attendance/update/<int:pk>/',
         views.AttendanceUpdateAPIView.as_view(), name="attendance_update"),
    path('attendance/delete/<int:pk>/',
         views.AttendanceDeleteAPIView.as_view(), name="attendance_delete"),



]
