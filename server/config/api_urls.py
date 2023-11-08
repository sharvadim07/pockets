from apps.pockets.routers import pockets_router
from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.users.urls.auth")),
    path("users/", include("apps.users.urls.users_urls")),
    path("pockets/", include(pockets_router.urls)),
]
