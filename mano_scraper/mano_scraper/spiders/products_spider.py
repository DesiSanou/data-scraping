import logging

import scrapy
import yaml
from yaml.loader import SafeLoader

PROJECT_ROOT = "/home/desire/Desktop/prv/wep_scraping/"

class ProductsSpider(scrapy.Spider):
    name = "products"
    def __init__(self):
        super(ProductsSpider, self).__init__()
        self.config = None

    def start_requests(self):
        self.get_config()
        self.build_urls()
        for url in self.config["urls"]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
            main_layout = response.css(self.config["page_main_div"])[0]
            logging.warning(type(main_layout))
            single_product_layout = self.config["single_product_layout"]
            products = main_layout.css(single_product_layout).getall()
            logging.warning("\n%r\n" % products)
            exit()
            for product in products:
                # yield  {field_key: product.css(field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_more_info"].items()}
                product_data = self.extract_info(product)
                logging.warning(product_data)

    def get_config(self, config_file=f"{PROJECT_ROOT}/data_config.yml"):
        with open(config_file) as f:
            self.config = yaml.load(f, Loader=SafeLoader)

    def extract_info(self, product):
        request = {field_key: self.config["single_product_info_div"] + " " + product.css(field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_info"].items()}
        more_info = {field_key: product.css(field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_more_info"].items()}
        request.update(more_info)
        #logging.warning("\n%r\n"%request)
        return request

    def build_urls(self):
        root_url = self.config["root_url"]
        self.config["urls"] = [root_url]
        for value in self.config["other_pages"]:
            page_url = root_url + "?" + self.config["page_slug"] + "=" + str(value)
            self.config["urls"].append(page_url)