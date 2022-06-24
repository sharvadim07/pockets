from decimal import Decimal

from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from ...constants import CategoryTypes


class TransactionQuerySet(QuerySet):
    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_income=Coalesce(
                Sum(
                    'amount',
                    filter=Q(category__category_type=CategoryTypes.INCOME),
                ),
                0,
                output_field=DecimalField(),
            ),
            total_expenses=Coalesce(
                Sum(
                    'amount',
                    filter=Q(category__category_type=CategoryTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ),
        )
