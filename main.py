import json
from classes.Price import Currency
from classes.Amazon import AmazonProduct
from classes.YandexMarket import MarketYandexProduct
from classes.Bestbuy import BestbuyProduct
from classes.Verkkokauppa import VerkkokauppaProduct


class Comparetor:
    def __init__(self, item):
        self.title = item["name"]
        self.amazon_product = AmazonProduct(item["amazon"])
        self.yandex_product = MarketYandexProduct(item["yandex"])
        self.bestbuy_product = BestbuyProduct(item["bestbuy"])
        self.verkkokauppa_product = VerkkokauppaProduct(item["verkkokauppa"])

    def __str__(self) -> str:
        return self.to_str(Currency.RUB)

    def profit(self, currency: Currency) -> float:
        if currency is Currency.USD:
            return self.yandex_product.usd_price - min(
                self.amazon_product.usd_price, self.bestbuy_product.usd_price
            )
        elif currency is Currency.EUR:
            return self.yandex_product.eur_price - min(
                self.amazon_product.eur_price, self.bestbuy_product.eur_price
            )
        elif currency is Currency.RUB:
            return self.yandex_product.rub_price - min(
                self.amazon_product.rub_price, self.bestbuy_product.rub_price
            )
        else:
            raise KeyError

    def to_str(self, currency: Currency) -> str:
        if currency is Currency.USD:
            return (f"{self.title}({self.profit(currency)}):\n\t"
                f"Amazon price: {self.amazon_product.usd_price}\t"
                f"Yandex price: {self.yandex_product.usd_price}\t"
                f"Bestbuy price: {self.bestbuy_product.usd_price}\t"
                f"Verkkokauppa price: {self.bestbuy_product.usd_price}\n")
        elif currency is Currency.EUR:
            return f"{self.title}({self.profit(currency)}):\n\tAmazon price: {self.amazon_product.eur_price}\tYandex price: {self.yandex_product.eur_price}\tBestbuy price: {self.bestbuy_product.eur_price}\n"
        elif currency is Currency.RUB:
            return (f"{self.title}({self.profit(currency)}):\n\t"
                f"Amazon: {self.amazon_product.rub_price}\t"
                f"Yandex: {self.yandex_product.rub_price}\t"
                f"Bestbuy: {self.bestbuy_product.rub_price}\t"
                f"Verkkokauppa: {self.verkkokauppa_product.rub_price}\n")
        else:
            raise KeyError


products = []
with open("data.csv") as f:
    f_json = json.load(f)

    for item in f_json:
        if item["type"] == "MacBook Pro 16":
            products.append(Comparetor(item))
            break

for product in products:
    try:
        print(product)
    except:
        pass
