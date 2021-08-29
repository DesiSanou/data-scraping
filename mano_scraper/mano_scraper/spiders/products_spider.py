import logging
import os

import scrapy
import yaml
from yaml.loader import SafeLoader


class ProductsSpider(scrapy.Spider):
    """
    Scrapy spider: defines how a the site (or a group of sites) will be scraped
    see https://docs.scrapy.org/en/latest/intro/tutorial.html for more details on scrapy

    """

    # defines spider name
    name = "products"

    # Customize the output file format and name
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'data/manamano_product.csv'}

    def __init__(self):
        super(ProductsSpider, self).__init__()
        self.config = None
        self.counter = 0

    def start_requests(self):
        """ Scrapy requests iterator."""
        self.get_config()
        self.build_urls()
        for url in self.config["urls"]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        Scrapy callback function called for each url visited. Parses the visited page

        :param response: response of a url request
        :param kwargs: additional parameters possible. see
        :return:
        """
        main_layout = response.css(self.config["page_main_div"])[0]
        single_product_layout = self.config["single_product_layout"]
        products = main_layout.css(single_product_layout)
        for product in products:
            product_data = self.extract_info(product)
            yield product_data
        self.counter += 1
        logging.warning("Scraping page number: %r\n" % (self.counter))

        if self.config["pages_list"] == [-1]:
            next_page_link_selector = self.config["next_page"] + " a::attr(href)"
            next_page = response.css(next_page_link_selector).getall()[-1]

            if self.counter == self.config["max_number_pages"]:
                next_page = None
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def get_config(self, config_file=f"../../../data_config.yml"):
        """
        Reads configuration from  from the define .yml file
        and updates de config instance variable

        :param config_file: path/to/config/file

        """
        with open(config_file) as f:
            self.config = yaml.load(f, Loader=SafeLoader)

    def extract_info(self, product: scrapy.selector.unified.Selector):
        """
        extract product info based on a product selector
        :param product: single product selector

        :return: extracted information dictionary
        """
        request = {field_key: product.css(self.config["single_product_info_div"] + " " + field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_info"].items()}
        more_info = {field_key: product.css(field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_more_info"].items()}
        request.update(more_info)
        return request

    def build_urls(self):
        """
        builds all urls of the pages to be scraped. add a 'urls' key to config dictionary
        """
        site_domain = self.config["site_domain"]
        section_root_url = site_domain + "/" + self.config["section_slug"]

        if self.config["pages_list"] == [-1]:
            self.config["urls"] = [section_root_url]
        else:
            self.config["urls"] = []
            for value in self.config["pages_list"]:
                page_url = section_root_url + "?" + self.config["page_slug"] + "=" + str(value)
                self.config["urls"].append(page_url)

