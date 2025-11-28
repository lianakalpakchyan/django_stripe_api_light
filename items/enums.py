from enum import Enum


class CurrencyEnum(Enum):
    USD = "USD"
    EUR = "EUR"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace("_", " ")) for key in cls]
