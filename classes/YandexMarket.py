import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from .Price import Currency, Price
from .Product import Product

load_dotenv()


r = requests.Session()
r.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}


yandex_headers = {
    "Host": "market.yandex.ru",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48",
}


def __preparation():
    r.get("https://market.yandex.ru", headers=yandex_headers)
    r.get("https://market.yandex.ru?pcr=213&contentRegion=2", headers=yandex_headers)


__preparation()


class MarketYandexProduct(Product):
    def __init__(self, link):
        self.link = link
        self.price = None
        self.name = None

        self._parse()

    def _parse(self):
        response = r.get(self.link, headers=yandex_headers)
        while 'action="/checkcaptcha"' in response.text:
            sudoPassword = os.getenv("SU_PASSWD")
            command = "service tor restart"
            os.system("echo %s|sudo -S %s" % (sudoPassword, command))
            print(r.get("https://api.ipify.org?format=json").text)
            response = r.get(self.link, headers=yandex_headers)
        soup = BeautifulSoup(response.text, "html.parser")

        price = None
        name = None
        try:
            price = (
                soup.find("div", {"class": "snippet-card__info"})
                .find("div", {"class": "snippet-card__price"})
                .find("div", {"class": "price"})
                .text.split("\xa0")[0]
                .replace(" ", "")
            )
            price = float(price)
            self.price = Price(price, Currency.RUB)
            name = soup.find("h1", {"class": "title title_size_22"}).find(
                "a", {"class": "link n-smart-link i-bem"}
            )
            self.name = name.text
        except AttributeError:
            pass


a = MarketYandexProduct(
    "https://market.yandex.ru/product--planshet-apple-ipad-2019-32gb-wi-fi/560271031/offers?glfilter=14871214%3A14897983&local-offers-first=1&how=aprice"
)
b = a
