from django.db import models

from ..models.managers.target_change_balance import TargetChangeBalanceManager


class TargetChangeBalance(models.Model):
    target: models.ForeignKey = models.ForeignKey(
        to="targets.Target",
        on_delete=models.CASCADE,
        related_name="changes_balance",
        verbose_name="Цель",
    )
    amount: models.DecimalField = models.DecimalField(
        verbose_name="Сумма",
        max_digits=10,
        decimal_places=2,
    )
    date: models.DateField = models.DateField(
        verbose_name="Дата изменения баланса",
        blank=True,
    )

    objects = TargetChangeBalanceManager()

    class Meta:
        verbose_name = "Изменние баланса цели"
        verbose_name_plural = "Изменния баланса цели"

    def __str__(self):
        return (
            f"TargetChangeBalance of Target {self.target.name}. Amount = {self.amount}"
        )
