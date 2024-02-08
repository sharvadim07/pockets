from apps.pockets.constants import TransactionErrors
from apps.pockets.models import TransactionCategory
from apps.pockets.serializers import TransactionCategorySerializer
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

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context["request"].user
        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        return category

    def create(self, validated_data: dict) -> Target:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
