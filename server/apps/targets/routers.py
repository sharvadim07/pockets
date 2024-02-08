from apps.targets.viewsets.target import TargetViewSet
from rest_framework.routers import DefaultRouter

targets_router = DefaultRouter()

targets_router.register(
    prefix="targets",
    viewset=TargetViewSet,
    basename="targets",
)
