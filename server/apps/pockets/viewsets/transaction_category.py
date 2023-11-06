from typing import Type

from django.db.models import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategoryTransactionSumSerializer,
)


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "transactions_by_categories":
            serializer_class = TransactionCategoryTransactionSumSerializer
        else:
            serializer_class = TransactionCategorySerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).order_by(
            "-id",
        )

        if self.action == "transactions_by_categories":
            queryset = queryset.annotate_with_transaction_sums()

        return queryset

    @action(methods=("GET",), detail=False, url_path="transactions-by-categories")
    def transactions_by_categories(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
