import scrapy
import logging
from scrapy import Request
from bs4 import BeautifulSoup
import json
import re

class GlobusSpider(scrapy.Spider):
    name = 'globus'
    allowed_domains = ['online.globus.ru']
    start_urls = ['https://online.globus.ru/catalog/molochnye-produkty-syr-yaytsa/kislomolochnye-produkty/smetana/?PAGEN_1=2']

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
        default_divs = response.css("div[product-js-template='PickerCategory']").extract()
        print(len(default_divs)) 
        for i, div in enumerate(default_divs):
            soup = BeautifulSoup(div, 'html.parser')
            divs = soup.find_all("div", {"product-js-template" : 'PickerCategory'})
            product_id = divs[0].attrs["data-sku"]
            titles = soup.find_all("span", class_="catalog-section__item__title")
            if titles:
                prices = soup.find_all("span", {"class" : "item-price__rub"})
                if prices:
                    print(titles[0].text)
                    weights = re.findall(r".+[^\d]{1}(\d+).{0,1}г", titles[0].text)
                    print(weights)
                    if weights:
                        title = titles[0].text
                        price = prices[0].text
                        weight = weights[0]
                        print(title, price,weight) 
                        self.products[product_id] = (title, price, weight)



        
        #price = response.css("span[data-testid='msrc-articles--article-price']::text").extract()
        #prices = response.xpath("//article/a/div/div[2]/div/div[1]/div/div/span/text()").extract()
        url = response.meta["splash"]["args"]["url"]
        logging.info(url)

        with open('smetana1.txt', 'w') as file:
            file.write(f"productid;title;price;weight\n")
            for k, v in self.products.items():
                title, price, weight = v
                file.write(f"{k};{title};{price};{weight}\n")


