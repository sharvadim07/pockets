from apps.users.views import UserCreateAPIView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UserCreateAPIView.as_view()),
    path("api-token-auth/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api-token-auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
