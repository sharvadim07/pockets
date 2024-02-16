from apps.targets.viewsets.target import TargetViewSet
from apps.targets.viewsets.target_change_balance import TargetChangeBalanceViewSet
from rest_framework.routers import DefaultRouter

targets_router = DefaultRouter()

targets_router.register(
    prefix="targets",
    viewset=TargetViewSet,
    basename="targets",
)
targets_router.register(
    prefix="target_changes_balance",
    viewset=TargetChangeBalanceViewSet,
    basename="target_changes_balance",
)
