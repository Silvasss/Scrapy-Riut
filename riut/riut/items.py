# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RiutItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Titulo = scrapy.Field()
    Autores = scrapy.Field()
    Orientadores = scrapy.Field()
    Palavraschaves = scrapy.Field()
    Datadocumento = scrapy.Field()
    Resumo = scrapy.Field()
    Repositorio = scrapy.Field()