from abc import abstractmethod
from copy import Error
from .Price import Price, Currency


class Product:
    price: Price
    name: str
    link: str

    @abstractmethod
    def _parse(self):
        pass

    @property
    def usd_price(self):
        try:
            return self.price.usd_price
        except:
            return None

    @property
    def rub_price(self):
        try:
            return self.price.rub_price
        except:
            return None

    @property
    def eur_price(self):
        try:
            return self.price.eur_price
        except:
            return None
