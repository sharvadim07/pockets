from typing import Final


class TransactionErrors:
    NOT_USERS_CATEGORY: Final[str] = "У пользователя нет такой категории"


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[
        str
    ] = "У пользоваетля уже существует категория с таким названием и типом"
