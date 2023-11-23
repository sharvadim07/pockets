from decimal import Decimal
from typing import Type, Union

from rest_framework import pagination, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionFilter
from ..models import Transaction
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    TransactionBalanceSerializer,
    TransactionCreateSerializer,
    TransactionGlobalSerializer,
    TransactionRetrieveSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    filterset_class = TransactionFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "total":
            serializer_class = TransactionGlobalSerializer
        elif self.action == "balance":
            serializer_class = TransactionBalanceSerializer
        elif self.action in {"create", "update", "partial_update"}:
            serializer_class = TransactionCreateSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:
        return (
            Transaction.objects.filter(
                user=self.request.user,
            )
            .select_related(
                "category",
            )
            .order_by(
                "-transaction_date",
                "-id",
            )
        )

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        if self.action == "total":
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            obj = queryset.aggregate_totals()
        elif self.action == "balance":
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            obj = queryset.get_balance()
        else:
            obj = super().get_object()

        return obj

    @action(methods=("GET",), detail=False, url_path="global")
    def total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=("GET",), detail=False, url_path="balance")
    def balance(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)
