from decimal import Decimal

from django.db.models import DecimalField, QuerySet, Sum
from django.db.models.functions import Coalesce


class TargetQuerySet(QuerySet):
    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_end_amount=Coalesce(
                Sum(
                    "end_amount",
                ),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_total_end_amount(self) -> dict[str, Decimal]:
        response_dict = {}
        totals_dict = self.aggregate_totals()
        response_dict["total_end_amount"] = totals_dict["total_end_amount"]
        return response_dict
