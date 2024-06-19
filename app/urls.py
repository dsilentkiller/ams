from django.urls import path, include
from app import views
urlpatterns = [
    path('subject/new/', views.SubjectCreateAPIView.as_view(), name="subject_create"),
    path('subject/list/', views.SubjectListAPIView.as_view(), name="subject_list"),
    path('subject/detail/<int:pk>/',
         views.SubjectDetailAPIView.as_view(), name="subject_detail"),
    path('subject/update/<int:pk>/',
         views.SubjectUpdateAPIView.as_view(), name="subject_update"),
    path('subject/delete/<int:pk>/',
         views.SubjectDeleteAPIView.as_view(), name="subject_delete"),


]
