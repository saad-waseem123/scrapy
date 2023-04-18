# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GigItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    level = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
