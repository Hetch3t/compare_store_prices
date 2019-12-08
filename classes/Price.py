from enum import Enum, auto

from forex_python.converter import CurrencyRates


rates = CurrencyRates()


class Currency(Enum):
    USD = auto()
    RUB = auto()
    EUR = auto()


class Price:
    _value: float
    _currency: Currency

    def __init__(self, value: float, currency: Currency) -> None:
        self._value = value
        self._currency = currency

    @property
    def usd_price(self) -> float:
        if self._currency is Currency.USD:
            return self._value
        elif self._currency is Currency.RUB:
            return self._value * rates.get_rate(Currency.RUB.name, Currency.USD.name)
        elif self._currency is Currency.EUR:
            return self._value * rates.get_rate(Currency.EUR.name, Currency.USD.name)
        else:
            raise KeyError

    @property
    def rub_price(self) -> float:
        if self._currency is Currency.USD:
            return self._value * rates.get_rate(Currency.USD.name, Currency.RUB.name)
        elif self._currency is Currency.RUB:
            return self._value
        elif self._currency is Currency.EUR:
            return self._value * rates.get_rate(Currency.EUR.name, Currency.RUB.name)
        else:
            raise KeyError

    @property
    def eur_price(self) -> float:
        if self._currency is Currency.USD:
            return self._value * rates.get_rate(Currency.USD.name, Currency.EUR.name)
        elif self._currency is Currency.RUB:
            return self._value * rates.get_rate(Currency.RUB.name, Currency.EUR.name)
        elif self._currency is Currency.EUR:
            return self._value
        else:
            raise KeyError
