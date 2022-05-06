# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ManhuaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = Field()
    title = Field()
    link = Field()

