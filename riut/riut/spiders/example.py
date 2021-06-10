import scrapy

#response.css(".metadataFieldValue ::text"
#response.css(".itemDisplayTable").get()

class ExampleSpider(scrapy.Spider):
    name = 'example'

    start_urls = ['https://repositorio.utfpr.edu.br/jspui/handle/1/20556']

    def parse(self, response):
        for post in response.css(".itemDisplayTable"):
            yield {
                "Titulo" : post.css(".metadataFieldValue ::text").get(),
                "Autor(es)" : post.css(".metadataFieldValue ::text")[1].get(),
                "Orientador(es)" : post.css(".metadataFieldValue ::text")[2].get(),
                "Palavras-chave": post.css(".subject ::text").getall(),
                "Data do documento" : post.css(".metadataFieldValue ::text")[9].get(),
                "Resumo" : post.css(".metadataFieldValue ::text")[10].get(),
                "Repositorio" : post.css(".metadataFieldValue ::text")[11].get()
            }
