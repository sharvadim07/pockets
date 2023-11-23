from django_filters import rest_framework as filters

from ..models import TransactionCategory


class TransactionCategoryFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=(
            ("transactions_expense_sum", "transactions_expense_sum"),
            # Add more fields for ordering as needed
        ),
    )

    class Meta:
        model = TransactionCategory
        fields = [
            "order_by",
        ]
