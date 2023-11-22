from django_filters import rest_framework as filters

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name="transaction_date", lookup_expr="year")
    year__gt = filters.NumberFilter(
        field_name="transaction_date", lookup_expr="year__gt"
    )
    year__lt = filters.NumberFilter(
        field_name="transaction_date", lookup_expr="year__lt"
    )

    month = filters.NumberFilter(field_name="transaction_date", lookup_expr="month")
    month__gt = filters.NumberFilter(
        field_name="transaction_date", lookup_expr="month__gt"
    )
    month__lt = filters.NumberFilter(
        field_name="transaction_date", lookup_expr="month__lt"
    )

    class Meta:
        model = Transaction
        fields = [
            "category",
            "year",
            "year__gt",
            "year__lt",
            "month",
            "month__gt",
            "month__lt",
        ]
