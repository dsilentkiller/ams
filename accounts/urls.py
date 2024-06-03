from django.urls import path, include
from accounts import views
urlpatterns = [
    path('api/token/', views.TokenObtainPairView, name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView, name='token_refresh'),
]
