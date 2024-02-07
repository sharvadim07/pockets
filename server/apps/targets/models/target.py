from django.db import models


class TargetModel(models.Model):
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
        default=0,
    )
    end_amount: models.DecimalField = models.DecimalField(
        verbose_name="Сколько хотите накопить",
    )
    term: models.DecimalField = models.DecimalField(
        verbose_name="Срок (месяцы)",
    )
    increase_percent: models.DecimalField = models.DecimalField(
        verbose_name="Процент",
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return f"{self.name} {self.category}"
