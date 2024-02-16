from datetime import datetime
from decimal import Decimal

from apps.targets.models.target import Target
from apps.targets.models.target_change_balance import TargetChangeBalance


def create_change_balance_now(target: Target, amount: Decimal) -> TargetChangeBalance:
    change_balance = TargetChangeBalance()
    change_balance.target = target
    change_balance.amount = amount
    change_balance.date = datetime.now()
    return change_balance


def get_target_balance(target: Target) -> Decimal:
    balance = Decimal("0.0")
    changes_balance = TargetChangeBalance.objects.filter(target=target)
    if changes_balance.exists():
        balance = changes_balance.get_balance()["balance"]
    return balance
