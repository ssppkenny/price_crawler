import scrapy
import logging
from scrapy import Request
from bs4 import BeautifulSoup
import json

class MigrosSpider(scrapy.Spider):
    name = 'migros'
    allowed_domains = ['produkte.migros.ch']
    start_urls = ['https://produkte.migros.ch/sortiment/supermarkt/lebensmittel/milchprodukte-eier/butter']

    products = dict()

    def __init__(self):
        self.html_file = open("file.html", "wb")

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })
        
    def parse(self, response):
        logging.info("request:")
        logging.info(response.meta["splash"]["args"]["url"])
        #titles = response.xpath("//article/a/@title").extract()
        default_divs = response.css("article[mode='default']").extract()
        for div in default_divs:
            soup = BeautifulSoup(div, 'html.parser')
            anchors = soup.find_all("a", {"data-testid" :"msrc-articles--article-link"})
            if anchors:
                spans = anchors[0].find_all("span", {"data-testid" : "msrc-articles--article-price"})
                if spans:
                    descrs = soup.find_all("p", {"data-testid": "msrc-articles--article-description"})
                    if descrs:
                        productids = soup.find_all("div", {"data-testid": "msrc-articles--add-to-shoppinglist"})
                        if productids:
                            title = anchors[0].attrs["title"]
                            price = spans[0].text
                            description = descrs[0].text
                            s = productids[0].attrs["data-setup"]
                            product_data = json.loads(s)
                            product_id = product_data["productId"]
                            self.products[product_id] = (title, price, description)


        
        #price = response.css("span[data-testid='msrc-articles--article-price']::text").extract()
        #prices = response.xpath("//article/a/div/div[2]/div/div[1]/div/div/span/text()").extract()
        #print(prices)
        url = response.meta["splash"]["args"]["url"]
        logging.info(url)
        url, *page = url.split("?")
        if page:
            _, number = page[0].split("=")
        else:
            number = 1
        new_url = 'https://produkte.migros.ch/sortiment/supermarkt/lebensmittel/milchprodukte-eier/butter' + "?page=" + str(int(number) + 1)
        params = {"page" : number}
        logging.info(new_url)
        if int(number) <= 0:
            yield scrapy.Request(new_url, self.parse, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': 0.5}
                    }
                }, dont_filter = True)
        else:
            with open('butter.txt', 'w') as file:
                for k, v in self.products.items():
                    title, price, description = v
                    file.write(f"{k};{title};{price};{description}\n")


