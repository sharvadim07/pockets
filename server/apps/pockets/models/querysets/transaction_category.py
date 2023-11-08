from django.db.models import DecimalField, QuerySet, Sum
from django.db.models.functions import Coalesce


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
