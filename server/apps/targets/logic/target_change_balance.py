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
