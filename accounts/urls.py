from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('send-email/', views.SendPasswordResetEmailAPIView.as_view(),
         name='send-email'),

    path('profile/', views.ProfileAPIView.as_view(),
         name='profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(),
         name='change-password')
    # path('api/token/', views.TokenObtainPairView, name='token_obtain_pair'),
    # path('api/token/refresh/', views.TokenRefreshView, name='token_refresh'),
]
