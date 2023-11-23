from django.db.models import DecimalField, Q, QuerySet, Sum
from django.db.models.functions import Coalesce

from ....pockets.constants import TransactionTypes


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            transactions_sum=Coalesce(
                Sum("transactions__amount"),
                0,
                output_field=DecimalField(),
            ),
        )

    def annotate_with_transaction_expense_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """
        return self.annotate(
            transactions_expense_sum=Coalesce(
                Sum(
                    "transactions__amount",
                    filter=Q(transactions__transaction_type=TransactionTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ),
        )
