from apps.pockets.constants import TransactionErrors
from apps.pockets.logic.transaction import create_expense_transaction_now
from apps.pockets.models import TransactionCategory
from apps.pockets.serializers import TransactionCategorySerializer
from apps.targets.models.target import Target
from apps.users.models import User
from rest_framework import serializers
from rest_framework.fields import Field

from server.apps.pockets.models.querysets.transaction import TransactionQuerySet


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

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context["request"].user
        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    def create(self, validated_data: dict) -> Target:
        validated_data["user"] = self.context["request"].user
        user = User.objects.get(validated_data["user"])
        start_amount = validated_data["start_amount"]
        category = TransactionCategory.objects.get(validated_data["category"])
        if start_amount > 0:
            transaction_queryset = TransactionQuerySet().filter(
                user=user,
            )
            balance = transaction_queryset.get_balance()
            if balance["balance"] >= start_amount:
                transaction = create_expense_transaction_now(
                    user=user,
                    category=category,
                    amount=start_amount,
                )
                transaction.save()
        else:
            transaction = create_expense_transaction_now(
                user=user,
                category=category,
                amount=start_amount,
            )
            transaction.save()
        return super().create(validated_data)
