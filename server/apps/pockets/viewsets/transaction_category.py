from typing import Type

from django.db.models import QuerySet
from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import TransactionCategoryFilter
from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategoryTransactionSumSerializer,
)


class TransactionCategoryViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    permission_classes = (IsAuthenticated,)
    filterset_class = TransactionCategoryFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "transactions_by_categories":
            serializer_class = TransactionCategoryTransactionSumSerializer
        else:
            serializer_class = TransactionCategorySerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        )

        if self.action == "list":
            queryset = (
                queryset.annotate_with_transaction_sums().annotate_with_transaction_expense_sums()
            )

        return queryset.order_by("-transactions_sum")

    @action(methods=("GET",), detail=False, url_path="transactions-by-categories")
    def transactions_by_categories(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
