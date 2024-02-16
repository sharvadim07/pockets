from django_filters import rest_framework as filters

from ..models.target import Target


class TargetFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="start_date")
    start_date__gt = filters.NumberFilter(
        field_name="start_date",
        lookup_expr="start_date__gt",
    )
    start_date__lt = filters.NumberFilter(
        field_name="start_date",
        lookup_expr="start_date__lt",
    )

    end_date = filters.DateFilter(field_name="end_date", lookup_expr="end_date")
    end_date__gt = filters.NumberFilter(
        field_name="end_date",
        lookup_expr="end_date__gt",
    )
    end_date__lt = filters.NumberFilter(
        field_name="end_date",
        lookup_expr="end_date__lt",
    )

    order_by = filters.OrderingFilter(
        fields=(
            ("category__name", "category"),
            ("start_date", "start_date"),
            ("end_date", "end_date"),
            ("start_amount", "start_amount"),
            ("end_amount", "end_amount"),
            ("increase_percent", "increase_percent"),
            # Add more fields for ordering as needed
        ),
    )

    class Meta:
        model = Target
        fields = [
            "category",
            "start_date",
            "start_date__gt",
            "start_date__lt",
            "end_date",
            "end_date__gt",
            "end_date__lt",
            "start_amount",
            "end_amount",
            "order_by",
        ]
