from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .managers import TransactionManager


class Transaction(models.Model):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Пользователь",
    )
    category = models.ForeignKey(
        to="pockets.TransactionCategory",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Категория",
    )
    transaction_date = models.DateField(
        verbose_name="Дата операции",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма операции",
        validators=(MinValueValidator(Decimal("0.01")),),
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self) -> str:
        return f"{self.category} {self.amount}"
