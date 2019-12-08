import requests
from bs4 import BeautifulSoup

from .Price import Currency, Price
from .Product import Product

r = requests.Session()


class VerkkokauppaProduct(Product):
    def __init__(self, link):
        self.link = link
        self.price = None

        self._parse()

    def _parse(self):
        response = r.get(
            self.link,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48",
            },
        )

        soup = BeautifulSoup(response.text, "html.parser")

        price = None
        try:
            price = soup.find("span", {"class": "price-tag-price__euros"})
            price = float(price.text.replace("\u202f", "").replace(",", "."))
            price = price / 1.24
            self.price = Price(price, Currency.EUR)
        except AttributeError:
            pass
