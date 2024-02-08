from apps.targets.models.target import Target
from apps.targets.serializers.target import (
    TargetCreateSerializer,
    TargetRetrieveSerializer,
)
from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated


class TargetViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    queryset = Target.objects.all()

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            serializer_class = TargetCreateSerializer
        else:
            serializer_class = TargetRetrieveSerializer
        return serializer_class
