from typing import Any

from apps.pockets.logic.transaction import create_income_transaction_now
from apps.targets.filters.target import TargetFilter
from apps.targets.models.querysets.target import TargetQuerySet
from apps.targets.models.target import Target
from apps.targets.serializers.target import (
    TargetCreateSerializer,
    TargetRetrieveSerializer,
)
from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class TargetViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    filterset_class = TargetFilter

    def get_queryset(self) -> TargetQuerySet:
        return (
            Target.objects.filter(
                user=self.request.user,
            )
            .select_related(
                "category",
            )
            .order_by(
                "-start_date",
            )
        )

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            serializer_class = TargetCreateSerializer
        else:
            serializer_class = TargetRetrieveSerializer
        return serializer_class

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.user
        # Check target balance an if it is lower than end amount
        # then create income transaction
        target = self.get_object()
        target_balance = target.changes_balance.get_queryset().get_balance()["balance"]
        if target_balance < target.end_amount:
            new_transaction = create_income_transaction_now(
                user=user,
                category=target.category,
                amount=target_balance,
            )
            new_transaction.save()
        return super().destroy(request, *args, **kwargs)
