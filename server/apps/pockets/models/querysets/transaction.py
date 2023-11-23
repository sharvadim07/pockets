from decimal import Decimal

from django.db.models import DecimalField, Q, QuerySet, Sum
from django.db.models.functions import Coalesce

from ...constants import TransactionTypes


class TransactionQuerySet(QuerySet):
    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_income=Coalesce(
                Sum(
                    "amount",
                    filter=Q(transaction_type=TransactionTypes.INCOME),
                ),
                0,
                output_field=DecimalField(),
            ),
            total_expenses=Coalesce(
                Sum(
                    "amount",
                    filter=Q(transaction_type=TransactionTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_balance(self) -> dict[str, Decimal]:
        response_dict = {}
        totals_dict = self.aggregate_totals()
        response_dict["balance"] = (
            totals_dict["total_income"] - totals_dict["total_expenses"]
        )
        return response_dict
