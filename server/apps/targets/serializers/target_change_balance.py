from apps.targets.models.target import Target
from rest_framework import serializers
from rest_framework.fields import Field

from server.apps.targets.serializers.target import TargetCreateSerializer


class TargetChangeBalanceRetrieveSerializer(serializers.ModelSerializer):
    target = TargetCreateSerializer(required=True)

    class Meta:
        model = Target
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
        model = Target
        fields = (
            "id",
            "target",
            "amount",
            "date",
        )
