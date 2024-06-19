from django.urls import path, include
from app import views
urlpatterns = [
    path('subject/', views.SubjectAPIView.as_view(), name="subject"),

]
