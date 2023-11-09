from typing import Final


class TransactionErrors:
    NOT_USERS_CATEGORY: Final[str] = "У пользователя нет такой категории"
    INCOME_TYPE_OF_TRANSACTION_WITH_CATEGORY: Final[
        str
    ] = "У транзакций с типом 'Доход' не может быть категории"
    EXPENSE_TYPE_OF_TRANSACTION_WITHOUT_CATEGORY: Final[
        str
    ] = "У транзакций с типом 'Расход' должна быть категория"


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[
        str
    ] = "У пользоваетля уже существует категория с таким названием и типом"
