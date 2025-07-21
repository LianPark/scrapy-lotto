# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LottoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    lmax = scrapy.Field()
    bc49 = scrapy.Field()
    dgrd = scrapy.Field()
    six49 = scrapy.Field()
    
    # lmax_date = scrapy.Field()
    # lmax_num = scrapy.Field()
    # lmax_bonus = scrapy.Field()

    # bc49_date = scrapy.Field()
    # bc49_num = scrapy.Field()
    # bc49_bonus = scrapy.Field()

    # six49_date = scrapy.Field()
    # six49_num = scrapy.Field()
    # six49_bonus = scrapy.Field()

    # dgrd_date = scrapy.Field()
    # dgrd_num = scrapy.Field()
    # dgrd_bonus = scrapy.Field()
    pass
