import scrapy
import logging
from scrapy import Request
from bs4 import BeautifulSoup
import json


def get_value(element, attribute, value, return_attribute, soup):
    elements = soup.find_all(element, {attribute : value})
    if elements:
        if return_attribute == "text":
            return elements[0].text
        elif return_attribute == "next":
            return elements[0].next_element
        else:
            return elements[0].attrs[return_attribute]
    else:
        return None

class CoopSpider(scrapy.Spider):
    name = 'coop'
    allowed_domains = ['coop.se']
    start_urls = ['https://www.coop.se/handla/varor/mejeri-agg/matlagningsmejerier/creme-fraiche-naturell']

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
        url = response.meta["splash"]["args"]["url"]
        product_containers = response.css("article[class='ItemTeaser js-product']").extract()
        
        for i, container in enumerate(product_containers):
            soup = BeautifulSoup(container, 'html.parser')

            scripts = soup.find_all("script", {"class": "js-model"})
            product = json.loads(scripts[0].contents[0])

            title = get_value("h3", "class", "ItemTeaser-heading", "text", soup)
            price = get_value("span", "class", "ItemTeaser-priceValue", "content", soup)
            weight = product["details"]["size"]["packageSizeInformation"]
            productid = product["id"]            
            print(title, price, weight, productid)
            if title and price and weight and productid:
                self.products[productid] = (title, price, weight)

        
        #price = response.css("span[data-testid='msrc-articles--article-price']::text").extract()
        #prices = response.xpath("//article/a/div/div[2]/div/div[1]/div/div/span/text()").extract()

        with open('creme-fraiche.txt', 'w') as file:
            file.write(f"productid;title;price;weight\n")
            for k, v in self.products.items():
                title, price, weight = v
                file.write(f"{k};{title};{price};{weight}\n")


