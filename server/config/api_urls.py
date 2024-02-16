from apps.pockets.routers import pockets_router
from apps.targets.routers import targets_router
from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.users.urls.auth")),
    path("users/", include("apps.users.urls.users_urls")),
    path("pockets/", include(pockets_router.urls)),
    path("targets/", include(targets_router.urls)),
]
