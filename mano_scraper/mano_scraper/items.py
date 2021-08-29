# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join



class ManoScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price_integer = scrapy.Field()
    price_decimal = scrapy.Field()
    price = get_price(price_integer, price_decimal)
    no_discount_price_integer = scrapy.Field()
    no_discount_price_decimal = scrapy.Field()
    no_discount_price = get_price(no_discount_price_integer, no_discount_price_decimal)
    rating = scrapy.Field(default=0, input_processor=MapCompose(str.strip, extract_rating), output_processor=TakeFirst())
    number_of_ratings = scrapy.Field(default=0, input_processor=MapCompose(int), output_processor=TakeFirst())
    url = scrapy.Field()
    brand = scrapy.Field()