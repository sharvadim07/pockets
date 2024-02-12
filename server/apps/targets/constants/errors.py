from typing import Final


class TargetErrors:
    ALREADY_EXISTS_TARGET_NAME: Final[str] = "Цель с таким именем уже существует"
    NOT_ENOUGH_BALANCE: Final[
        str
    ] = "Недостаточный баланс для создания цели с такой стартовой суммой"
