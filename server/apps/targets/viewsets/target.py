from typing import Any

from apps.pockets.logic.transaction import (
    create_expense_transaction_now,
    create_income_transaction_now,
)
from apps.targets.filters.target import TargetFilter
from apps.targets.logic.target_change_balance import create_change_balance_now
from apps.targets.models.querysets.target import TargetQuerySet
from apps.targets.models.target import Target
from apps.targets.serializers.target import (
    TargetCreateSerializer,
    TargetRetrieveSerializer,
    TargetTopUpSerializer,
)
from rest_framework import pagination, status, viewsets
from rest_framework.decorators import action
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

    def perform_create(self, serializer) -> None:
        target = serializer.save()
        transaction = create_expense_transaction_now(
            user=target.user,
            category=target.category,
            amount=target.start_amount,
        )
        change_balance = create_change_balance_now(
            target=target,
            amount=target.start_amount,
        )
        transaction.save()
        change_balance.save()

    @action(methods=("PATCH",), detail=True, url_path="topup")
    def topup(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        target = self.get_object()
        serializer = TargetTopUpSerializer(data=request.data, instance=target)
        if serializer.is_valid():
            transaction = create_expense_transaction_now(
                user=user,
                category=target.category,
                amount=serializer.validated_data["amount"],
            )
            change_balance = create_change_balance_now(
                target=target,
                amount=serializer.validated_data["amount"],
            )
            transaction.save()
            change_balance.save()
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
