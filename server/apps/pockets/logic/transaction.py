from datetime import datetime
from decimal import Decimal
from typing import Optional

from apps.pockets.constants import TransactionTypes
from apps.pockets.models import Transaction
from apps.pockets.models.transaction_category import TransactionCategory
from apps.users.models.user import User


def create_expense_transaction_now(
    user: User, category: Optional[TransactionCategory], amount: Decimal
) -> Transaction:
    transaction = Transaction()
    transaction.user = user
    transaction.category = category
    transaction.amount = amount
    transaction.transaction_date = datetime.now()
    transaction.transaction_type = TransactionTypes.EXPENSE
    return transaction


def create_income_transaction_now(
    user: User, category: Optional[TransactionCategory], amount: Decimal
) -> Transaction:
    transaction = Transaction()
    transaction.user = user
    transaction.category = category
    transaction.amount = amount
    transaction.transaction_date = datetime.now()
    transaction.transaction_type = TransactionTypes.INCOME
    return transaction
