## E-commerce Website  Scraper

This scraper is used to get multiple information on products.  
Parameters are defined in a yaml file (data_config.yml).
You can run the process via scrapy command line.
This implementation is based on scrapy. For more information on scrapy, see https://docs.scrapy.org/en/latest/index.html

information:
- Url of the product
- Title
- Brand
- Price
- Rating
- Number of ratings
- no discount price

#### Note : An additional field was added called no_discount_price

Tested on would scrap manomano.fr to study its  catalog drill section

It can be adapted for other information or other section but not tested yet.
The scrapped data is saved in folder called data

Python version used: 3.7.5

To run the code:
Assuming you are in the project root folder.
``` 
> pip3 install -r requirements.txt # install scrapy and pyaml
> cd mano_scraper/mano_scraper/spiders
> scrapy crawl products # run the spider 'products'
```
