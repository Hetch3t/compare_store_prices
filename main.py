import json

from classes.Amazon import AmazonProduct
from classes.YandexMarket import MarketYandexProduct
from classes.Bestbuy import BestbuyProduct


class Comparetor:
    def __init__(self, item):
        try:
            self.amazon_product = AmazonProduct(item["amazon"])
            self.yandex_product = MarketYandexProduct(item["yandex"])
            self.bestbuy_product = BestbuyProduct(item["bestbuy"])
        except:
            pass

    def __str__(self):
        return f"Amazon price: {self.amazon_product.usd_price}\t\
                Yandex price: {self.yandex_product.usd_price}\t\
                Bestbuy price: {self.bestbuy_product.usd_price}"

    @property
    def profit(self):
        return self.yandex_product.usd_price - self.amazon_product.usd_price

    @property
    def profit_percent(self):
        return (
            self.yandex_product.usd_price - self.amazon_product.usd_price
        ) / self.amazon_product.usd_price


products = []
with open("data.csv") as f:
    f_json = json.load(f)
    for item in f_json:
        products.append(Comparetor(item))

for product in products:
    print(product)
