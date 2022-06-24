from django.urls import path
from rest_framework.authtoken import views

from apps.users.views import UserCreateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
]
