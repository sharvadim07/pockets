from decimal import Decimal

from apps.pockets.constants import TransactionErrors
from apps.pockets.logic.transaction import create_expense_transaction_now
from apps.pockets.models import TransactionCategory
from apps.pockets.models.transaction import Transaction
from apps.pockets.serializers import TransactionCategorySerializer
from apps.targets.constants.errors import TargetErrors
from apps.targets.logic.target_change_balance import create_change_balance_now
from apps.targets.models.target import Target
from rest_framework import serializers
from rest_framework.fields import Field


class TargetRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer(required=False)

    class Meta:
        model = Target
        fields = (
            "id",
            "name",
            "category",
            "start_amount",
            "end_amount",
            "term",
            "increase_percent",
        )


class TargetCreateSerializer(serializers.ModelSerializer):
    category: Field = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Target
        fields = (
            "id",
            "name",
            "category",
            "start_amount",
            "end_amount",
            "term",
            "increase_percent",
        )

    def validate_name(self, name: str) -> str:
        user = self.context["request"].user
        tragets = user.targets.all()
        if name in {target.name for target in tragets}:
            raise serializers.ValidationError(TargetErrors.ALREADY_EXISTS_TARGET_NAME)
        return name

    def validate_start_amount(self, start_amount: Decimal) -> Decimal:
        user = self.context["request"].user
        if start_amount > 0:
            transaction_queryset = Transaction.objects.filter(
                user=user,
            )
            balance = transaction_queryset.get_balance()
            if balance["balance"] < start_amount:
                raise serializers.ValidationError(TargetErrors.NOT_ENOUGH_BALANCE)
        return start_amount

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context["request"].user
        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    def create(self, validated_data: dict) -> Target:
        validated_data["user"] = self.context["request"].user
        user = validated_data["user"]
        start_amount = validated_data["start_amount"]
        category = validated_data["category"] if "category" in validated_data else None
        transaction = create_expense_transaction_now(
            user=user,
            category=category,
            amount=start_amount,
        )
        target = super().create(validated_data)
        change_balance = create_change_balance_now(
            target=target,
            amount=start_amount,
        )
        transaction.save()
        change_balance.save()
        return target
