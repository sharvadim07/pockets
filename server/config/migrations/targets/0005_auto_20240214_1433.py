# Generated by Django 3.2.2 on 2024-02-14 11:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("targets", "0004_auto_20240214_1226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="target",
            name="end_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Дата завершения цели"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="target",
            name="start_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Дата создания цели"
            ),
            preserve_default=False,
        ),
    ]