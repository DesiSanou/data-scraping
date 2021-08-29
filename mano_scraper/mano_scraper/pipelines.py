# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter


def extract_rating(raw_rating):
    value = float(raw_rating.split("/")[0])
    return round(value, 1)


def get_price(price_integer, price_decimal):
    if price_integer and price_decimal:
        return float(price_integer) + float(price_decimal)/100
    else:
        return None


def get_brand(alt_text):
    txt = alt_text.strip()
    brand = txt.split(' ')[-1]
    brand = brand.strip('"')
    logging.warning(brand)
    return brand


class ManoScraperPipeline:
    def process_item(self, item, spider):
        item['url'] = spider.config['site_domain'] + item["url"]
        item["rating"] = extract_rating(item["rating"])
        item['price'] = get_price(item['price_integer'], item["price_decimal"])
        item['no_discount_price'] = get_price(item['no_discount_price_integer'], item["no_discount_price_decimal"])
        item["brand"] = get_brand(item["brand"])
        item["number_of_ratings"] = int(item["number_of_ratings"])
        del item['price_integer']
        del item['price_decimal']
        del item['no_discount_price_integer']
        del item["no_discount_price_decimal"]
        return item
