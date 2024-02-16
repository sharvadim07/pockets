from decimal import Decimal

from django.db.models import Manager

from ..querysets.target import TargetQuerySet


class TargetManager(Manager):
    def get_queryset(self, **kwargs) -> TargetQuerySet:
        return TargetQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_target_sums(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()
