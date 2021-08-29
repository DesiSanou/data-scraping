import scrapy
import yaml
from yaml.loader import SafeLoader

PROJECT_ROOT = "/home/desire/Desktop/prv/wep_scraping/"
# TODO: clean scarped data, convert special characters to readable data,

class ProductsSpider(scrapy.Spider):
    name = "products"
    custom_settings = {'FEED_FORMAT': 'json', 'FEED_URI': 'manamano_product.json'}

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
        single_product_layout = self.config["single_product_layout"]
        products = main_layout.css(single_product_layout)

        for product in products:
            product_data = self.extract_info(product)

            yield product_data

    def get_config(self, config_file=f"{PROJECT_ROOT}/data_config.yml"):
        with open(config_file) as f:
            self.config = yaml.load(f, Loader=SafeLoader)

    def extract_info(self, product):
        request = {field_key: product.css(self.config["single_product_info_div"] + " " + field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_info"].items()}
        more_info = {field_key: product.css(field_info['css']+"::" + field_info["type"]).get() for field_key, field_info in self.config["product_more_info"].items()}
        request.update(more_info)
        return request

    def build_urls(self):
        site_domain = self.config["site_domain"]
        section_root_url = site_domain + self.config["section_slug"]
        self.config["urls"] = [section_root_url]
        for value in self.config["other_pages"]:
            page_url = section_root_url + "?" + self.config["page_slug"] + "=" + str(value)
            self.config["urls"].append(page_url)

    def clean_data(self, product_data):
        pass