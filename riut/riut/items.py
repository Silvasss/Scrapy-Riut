# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RiutItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    titulo = scrapy.Field()
    autores = scrapy.Field()
    orientadores = scrapy.Field()
    palavraschaves = scrapy.Field()
    datadocumento = scrapy.Field()
    resumo = scrapy.Field()
    repositorio = scrapy.Field()
    pass
