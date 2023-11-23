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
    TransactionCategoryTopExpenseCategory,
)


class TransactionCategoryViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    permission_classes = (IsAuthenticated,)
    filterset_class = TransactionCategoryFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "top_expense":
            serializer_class = TransactionCategoryTopExpenseCategory
        else:
            serializer_class = TransactionCategorySerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        )
        queryset = queryset.annotate_with_transaction_expense_sums()
        queryset = queryset.order_by("-transactions_expense_sum")
        return queryset

    def get_top_expense_categories(self, categories, num=3):
        sorted_categories = sorted(
            categories, key=lambda v: v["transactions_expense_sum"], reverse=True
        )
        top_expense_categories = sorted_categories[:num]
        other_categories = sorted_categories[num:]
        other_categories_expense_sum = sum(
            float(category["transactions_expense_sum"]) for category in other_categories
        )
        top_expense_categories.append(
            {
                "name": "Другое",
                "transactions_expense_sum": f"{other_categories_expense_sum:.2f}",
            }
        )
        return top_expense_categories

    @action(methods=("GET",), detail=False, url_path="top_expense")
    def top_expense(self, request: Request, *args, **kwargs) -> Response:
        response = super().list(request, *args, **kwargs)
        top_expense_categories = self.get_top_expense_categories(
            categories=response.data
        )
        response.data = top_expense_categories
        return response
