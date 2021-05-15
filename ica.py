import scrapy


class IcaSpider(scrapy.Spider):
    name = 'ica'
    allowed_domains = ['ica.se']
    start_urls = ['http://ica.se/']

    def parse(self, response):
        pass
