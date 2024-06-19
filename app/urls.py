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

]
