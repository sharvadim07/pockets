from typing import Final


class TargetErrors:
    ALREADY_EXISTS_TARGET_NAME: Final[str] = "Цель с таким именем уже существует"
    NOT_ENOUGH_BALANCE: Final[str] = "Недостаточный баланс для пополнения цели"
    END_AMOUNT_LOWER_THAN_BALANCE: Final[str] = "Целевая сумма меньше чем баланс цели"
    END_AMOUNT_NOT_ACHIEVED: Final[str] = "Целевая сумма не достигнута"
