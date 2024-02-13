from decimal import Decimal

from django.db.models import Manager

from ..querysets.target_change_balance import TargetChangeBalanceQuerySet


class TargetChangeBalanceManager(Manager):
    def get_queryset(self, **kwargs) -> TargetChangeBalanceQuerySet:
        return TargetChangeBalanceQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_transaction_sums(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()
