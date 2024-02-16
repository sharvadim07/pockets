from decimal import Decimal

from django.db.models import DecimalField, QuerySet, Sum
from django.db.models.functions import Coalesce


class TargetChangeBalanceQuerySet(QuerySet):
    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_change=Coalesce(
                Sum(
                    "amount",
                ),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_balance(self) -> dict[str, Decimal]:
        response_dict = {}
        totals_dict = self.aggregate_totals()
        response_dict["balance"] = totals_dict["total_change"]
        return response_dict
