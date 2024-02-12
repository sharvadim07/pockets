from apps.targets.models.target_change_balance import TargetChangeBalance
from apps.targets.serializers.target_change_balance import (
    TargetChangeBalanceCreateSerializer,
    TargetChangeBalanceRetrieveSerializer,
)
from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated


class TargetChangeBalanceViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    queryset = TargetChangeBalance.objects.all()

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            serializer_class = TargetChangeBalanceCreateSerializer
        else:
            serializer_class = TargetChangeBalanceRetrieveSerializer
        return serializer_class
