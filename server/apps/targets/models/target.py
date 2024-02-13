from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Target(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="targets",
        verbose_name="Пользователь",
    )
    category: models.ForeignKey = models.ForeignKey(
        to="pockets.TransactionCategory",
        on_delete=models.CASCADE,
        related_name="targets",
        verbose_name="Категория",
        null=True,
        blank=True,
    )
    name: models.CharField = models.CharField(
        max_length=40,
        verbose_name="Имя цели",
        null=False,
        blank=False,
    )
    start_amount: models.DecimalField = models.DecimalField(
        verbose_name="Начальная сумма",
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal("0.0")),),
        default=Decimal("0.0"),
    )  # type: ignore
    end_amount: models.DecimalField = models.DecimalField(
        verbose_name="Сколько хотите накопить",
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal("0.01")),),
    )
    term: models.IntegerField = models.IntegerField(
        verbose_name="Срок (месяцы)",
        validators=(MinValueValidator(Decimal("1")),),
    )
    increase_percent: models.DecimalField = models.DecimalField(
        verbose_name="Процент",
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal("0.01")),),
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return f"Target {self.name} of {self.category}"
