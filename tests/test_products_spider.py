import logging
import unittest
from mano_scraper.mano_scraper.spiders.products_spider import ProductsSpider


class ProductsSpiderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.product_spider = ProductsSpider()
        self.product_spider.get_config()

    def test_get_config_file(self):
        self.assertEqual(isinstance(self.product_spider.config, dict), True)  # add assertion here
        self.assertEqual(self.product_spider.config["root_url"], "https://www.manomano.fr/perceuse-1146")
        self.assertEqual(self.product_spider.config["other_pages"], [2, 3])
        logging.warning(self.product_spider.config)

    def test_build_urls(self):
        self.product_spider.build_urls()
        self.assertListEqual(self.product_spider.config["urls"], ['https://www.manomano.fr/perceuse-1146',
                                                                  'https://www.manomano.fr/perceuse-1146?page=2',
                                                                  'https://www.manomano.fr/perceuse-1146?page=3'])
        logging.warning(self.product_spider.config["urls"])

    def test_extract_info(self):
        pass


if __name__ == '__main__':
    unittest.main()
