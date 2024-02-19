from decimal import Decimal
from typing import Any

from apps.pockets.logic.transaction import (
    create_expense_transaction_now,
    create_income_transaction_now,
)
from apps.pockets.models.transaction import Transaction
from apps.targets.filters.target import TargetFilter
from apps.targets.logic.target_change_balance import (
    create_change_balance_now,
    get_target_balance,
)
from apps.targets.models.querysets.target import TargetQuerySet
from apps.targets.models.target import Target
from apps.targets.models.target_change_balance import TargetChangeBalance
from apps.targets.serializers.target import (
    TargetBalanceSerializer,
    TargetCreateSerializer,
    TargetFinishSerializer,
    TargetRetrieveSerializer,
    TargetTopUpSerializer,
)
from apps.users.models.user import User
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
        elif self.action == "balance":
            serializer_class = TargetBalanceSerializer
        else:
            serializer_class = TargetRetrieveSerializer
        return serializer_class

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user: User = request.user
        # Check target balance an if it is lower than end amount
        # then create income transaction
        target: Target = self.get_object()
        target_balance: Decimal = get_target_balance(target=target)
        if target_balance < target.end_amount:
            new_transaction = create_income_transaction_now(
                user=user,
                category=target.category,
                amount=target_balance,
            )
            new_transaction.save()
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        target: Target = serializer.save()
        transaction: Transaction = create_expense_transaction_now(
            user=target.user,
            category=target.category,
            amount=target.start_amount,
        )
        change_balance: TargetChangeBalance = create_change_balance_now(
            target=target,
            amount=target.start_amount,
        )
        transaction.save()
        change_balance.save()

    def get_object(self) -> Any:
        if self.action == "balance":
            target: Target = super().get_object()
            return {"balance": get_target_balance(target=target)}
        else:
            return super().get_object()

    @action(methods=("PATCH",), detail=True, url_path="topup")
    def topup(self, request: Request, *args, **kwargs) -> Response:
        user: User = request.user
        target: Target = self.get_object()
        serializer: TargetTopUpSerializer = TargetTopUpSerializer(
            data=request.data, instance=target
        )
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

    @action(methods=("PATCH",), detail=True, url_path="finish")
    def finish(self, request: Request, *args, **kwargs) -> Response:
        user: User = request.user
        target: Target = self.get_object()
        serializer: TargetFinishSerializer = TargetFinishSerializer(
            data=request.data, instance=target
        )
        if serializer.is_valid():
            transaction = create_income_transaction_now(
                user=user,
                category=target.category,
                amount=serializer.validated_data["target_balance"],
            )
            change_balance = create_change_balance_now(
                target=target,
                amount=-serializer.validated_data["target_balance"],
            )
            transaction.save()
            change_balance.save()
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=("GET",), detail=True, url_path="balance")
    def balance(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)
