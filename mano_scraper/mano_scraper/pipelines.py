# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


def extract_rating(raw_rating):
    """
    extract real rating from rates of form x/y i.e. 4/5 will return 4

    :param raw_rating:

    :return: rating in float
    """
    if raw_rating:
        value = float(raw_rating.split("/")[0])
        return round(value, 1)
    else:
        return None


def get_price(price_integer, price_decimal):
    """
    As prices are in different selectors, this function combine them to get the final price

    :param price_integer: integer value of price
    :param price_decimal: decimal part of price

    :return: return final price
    """
    if price_integer:
        if not price_decimal:
            price_decimal = 0
        price_integer = price_integer.split(' ') # Useful for value > 999
        price_integer = "".join(price_integer)
        return float(price_integer) + float(price_decimal)/100
    else:
        return None


def get_brand(alt_text):
    """
     Extract brand name from image field alt attribute text

    :param alt_text: alt complete string

    :return: extracted brand name
    """
    if alt_text:
        txt = alt_text.strip()
        brand = txt.split(' ')[-1]
        brand = brand.strip('"')
    else:
        brand = None
    return brand


def get_number_of_ratings(number_of_ratings_str):
    """

    :param number_of_ratings_str: string of number of ratings

    :return: casted value in int. None if string is empty .
    """
    return int(number_of_ratings_str) if number_of_ratings_str else None


class ManoScraperPipeline:
    def process_item(self, item, spider):
        """
        Called form each product extracted for data cleaning purpose.

        :param item: single product dictionary
        :param spider:
        :return:
        """
        item['url'] = spider.config['site_domain'] + item["url"]
        item["rating"] = extract_rating(item["rating"])
        item['price'] = get_price(item['price_integer'], item["price_decimal"])
        item['no_discount_price'] = get_price(item['no_discount_price_integer'], item["no_discount_price_decimal"])
        item["brand"] = get_brand(item["brand"])
        item["number_of_ratings"] = get_number_of_ratings(item["number_of_ratings"])
        del item['price_integer']
        del item['price_decimal']
        del item['no_discount_price_integer']
        del item["no_discount_price_decimal"]
        return item
