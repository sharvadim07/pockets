from datetime import datetime

from apps.pockets.constants import TransactionTypes
from apps.pockets.models import Transaction


def create_expense_transaction_now(user, category, amount) -> Transaction:
    transaction = Transaction()
    transaction.user = user
    transaction.category = category
    transaction.amount = amount
    transaction.transaction_date = datetime.now()
    transaction.transaction_type = TransactionTypes.EXPENSE
    return transaction
