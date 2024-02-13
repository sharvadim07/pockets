from apps.targets.models.target import Target
from apps.targets.models.target_change_balance import TargetChangeBalance
from apps.targets.serializers.target import TargetCreateSerializer
from rest_framework import serializers
from rest_framework.fields import Field


class TargetChangeBalanceRetrieveSerializer(serializers.ModelSerializer):
    target = TargetCreateSerializer(required=True)

    class Meta:
        model = TargetChangeBalance
        fields = (
            "id",
            "target",
            "amount",
            "date",
        )


class TargetChangeBalanceCreateSerializer(serializers.ModelSerializer):
    target: Field = serializers.PrimaryKeyRelatedField(
        queryset=Target.objects.all(),
        allow_null=False,
        required=True,
    )

    class Meta:
        model = TargetChangeBalance
        fields = (
            "id",
            "target",
            "amount",
            "date",
        )
