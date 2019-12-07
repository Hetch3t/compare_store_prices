from bs4 import BeautifulSoup
import requests

r = requests.Session()
r.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}

print(r.get("https://api.ipify.org?format=json").text)
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
r.get("https://market.yandex.ru", headers=yandex_headers)
r.get("https://market.yandex.ru?pcr=213&contentRegion=2", headers=yandex_headers)


class Product:
    def __init__(self, line):
        [self.amazon_link, self.yandex_link] = line.split("    ")
        self.amazon_price = self._amazon_parse()
        [self.yandex_price, self.name] = self._yandex_parse()

    def __str__(self):
        return f"Amazon price: {self.amazon_price}\tYandex price: {self.yandex_price}\tProfit: {self.profit_percent}"

    @property
    def profit(self):
        return self.yandex_price - self.amazon_price

    @property
    def profit_percent(self):
        return (self.yandex_price - self.amazon_price) / self.amazon_price

    def _amazon_parse(self):
        response = r.get(
            self.amazon_link,
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
            price = soup.find("span", {"id": "priceblock_ourprice"})
            price = float(price.text[1:])
        except AttributeError:
            pass

        return price

    def _yandex_parse(self):
        response = r.get(self.yandex_link, headers=yandex_headers)

        soup = BeautifulSoup(response.text, "html.parser")

        price = None
        name = None
        try:
            price = (
                soup.find("div", {"class": "snippet-card__info"})
                .find("div", {"class": "price"})
                .text
            )
            name = soup.find(
                "a",
                {
                    "class": "link n-smart-link i-bem n-smart-link_js_inited link_js_inited"
                },
            )
        except KeyError:
            pass

        return [price, name]


products = []
with open("data.csv") as f:
    f.readline()
    for line in f:
        products.append(Product(line.strip()))

print(products)
