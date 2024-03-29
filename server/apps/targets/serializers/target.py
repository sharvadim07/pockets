from datetime import date
from decimal import Decimal

from apps.pockets.constants import TransactionErrors
from apps.pockets.logic.transaction import get_user_balance
from apps.pockets.models import TransactionCategory
from apps.pockets.serializers import TransactionCategorySerializer
from apps.targets.constants.errors import TargetErrors
from apps.targets.logic.target_change_balance import get_target_balance
from apps.targets.models.target import Target
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator
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
            "start_date",
            "end_date",
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
        if start_amount > 0 and get_user_balance(user) < start_amount:
            raise serializers.ValidationError(TargetErrors.NOT_ENOUGH_BALANCE)
        return start_amount

    def validate_end_amount(self, end_amount: Decimal) -> Decimal:
        target = self.instance
        if target and get_target_balance(target) > end_amount:
            raise serializers.ValidationError(
                TargetErrors.END_AMOUNT_LOWER_THAN_BALANCE
            )
        return end_amount

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context["request"].user
        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    def create(self, validated_data: dict) -> Target:
        user = self.context["request"].user
        validated_data["user"] = user

        # Set start and end dates for target
        if "start_date" not in validated_data:
            validated_data["start_date"] = date.today()
        validated_data["end_date"] = validated_data["start_date"] + relativedelta(
            months=+validated_data["term"],
        )
        return super().create(validated_data)


class TargetTopUpSerializer(serializers.Serializer):
    class Meta:
        model = Target

    amount: serializers.DecimalField = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal("0.0")),),
    )

    def validate_amount(self, amount: Decimal) -> Decimal:
        user = self.instance.user
        if amount > 0 and get_user_balance(user) < amount:
            raise serializers.ValidationError(TargetErrors.NOT_ENOUGH_BALANCE)
        return amount


class TargetFinishSerializer(serializers.Serializer):
    class Meta:
        model = Target

    def validate(self, attrs):
        target: Target = self.instance
        target_balance: Decimal = get_target_balance(target=target)
        if target and target_balance < target.end_amount:
            raise serializers.ValidationError(
                TargetErrors.END_AMOUNT_NOT_ACHIEVED,
            )
        attrs["target_balance"] = target_balance
        return super().validate(attrs)


class TargetBalanceSerializer(serializers.Serializer):
    balance: serializers.DecimalField = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
