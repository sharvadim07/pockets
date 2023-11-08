from collections import OrderedDict

from rest_framework import serializers

from ..constants import TransactionErrors
from ..constants.errors import TransactionCategoryErrors
from ..constants.transaction import TransactionTypes
from ..models import Transaction, TransactionCategory
from .transaction_category import TransactionCategorySerializer


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = ("id", "category", "transaction_date", "amount", "transaction_type")


class TransactionCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Transaction
        fields = ("id", "category", "transaction_date", "amount", "transaction_type")

    def validate(self, attrs):
        if attrs["transaction_type"] == TransactionTypes.INCOME:
            raise serializers.ValidationError(
                TransactionCategoryErrors.INCOME_TYPE_OF_TRANSACTION
            )
        else:
            return attrs

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context["request"].user
        print("validate_category")
        if category not in user.categories.all():
            raise serializers.ValidationError(TransactionErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def create(self, validated_data: dict) -> Transaction:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        Сделано для того, чтобы при создании объекта можно было передвавть id категории, а после
        создания поле категории возвращалось как объект
        """
        return TransactionRetrieveSerializer(instance=self.instance).data


class TransactionGlobalSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
