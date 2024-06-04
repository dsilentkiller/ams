from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    # path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register', views.RegisterAPIView.as_view(), name='register'),
    # path('api/token/', views.TokenObtainPairView, name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView, name='token_refresh'),
]
