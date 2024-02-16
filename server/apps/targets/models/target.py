from decimal import Decimal

from apps.targets.models.managers.target import TargetManager
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
        validators=(MinValueValidator(Decimal("0.0")),),
    )
    term: models.IntegerField = models.IntegerField(
        verbose_name="Срок (месяцы)",
        validators=(MinValueValidator(Decimal("1")),),
    )
    increase_percent: models.DecimalField = models.DecimalField(
        verbose_name="Процент",
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal("0.0")),),
    )
    start_date: models.DateField = models.DateField(
        verbose_name="Дата создания цели",
    )
    end_date: models.DateField = models.DateField(
        verbose_name="Дата завершения цели",
    )

    objects = TargetManager()

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return f"Target {self.name} of {self.category}"
