import scrapy

# https://repositorio.utfpr.edu.br/jspui/handle/1/20556
# response.css("tr ::text").getall()

class ExampleSpider(scrapy.Spider):
    name = 'example'

    start_urls = ["https://repositorio.utfpr.edu.br/jspui/handle/1/20556"]

    def parse(self, response):
        camposInteresse = ["Título:", "Autor(es):", "Orientador(es):", "Data do documento:", "Resumo:", "URI:"]

        # Dicionario temporario
        dictAux = {}

        for post in response.css("tr"):
            aux = post.css("::text").get()

            try:
                if any(i in aux for i in camposInteresse):
                    dictAux[post.css("::text")[0].get()] = post.css("::text")[1].get()
                elif "Palavras-chave:" in aux:
                    dictAux[post.css("::text")[0].get()] = post.css("::text")[1:].getall()
            except NameError:
                pass

        yield {
            "Título" : dictAux["Título:\xa0"],
            "Autor(es)" : dictAux["Autor(es):\xa0"],
            "Orientador(es)" : dictAux["Orientador(es):\xa0"],
            "Palavras-chave" : dictAux["Palavras-chave:\xa0"],
            "Data do documento" : dictAux["Data do documento:\xa0"],
            "Resumo" : dictAux["Resumo:\xa0"],
            "Repositorio" : dictAux["URI:\xa0"]
        }