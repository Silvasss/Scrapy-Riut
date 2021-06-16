import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ExampleSpider(scrapy.Spider):
    name = 'example'

    start_urls = []

    # Criando os links dos repositorios
    for i in range(0, 25300):
        start_urls.append("https://repositorio.utfpr.edu.br/jspui/handle/1/{}".format(i))

    # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, callback = self.parse, errback = self.errback_httpbin, dont_filter = True)

    # Faz acontece, caso nao ocorra nenhum erro
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

        # Erro em alguns por nao localizar o "Orientador(es):\xa0"
        yield {
            "Título" : dictAux["Título:\xa0"],
            "Autor(es)" : dictAux["Autor(es):\xa0"],
            "Orientador(es)" : dictAux["Orientador(es):\xa0"],
            "Palavras-chave" : dictAux["Palavras-chave:\xa0"],
            "Data do documento" : dictAux["Data do documento:\xa0"],
            "Resumo" : dictAux["Resumo:\xa0"],
            "Repositorio" : dictAux["URI:\xa0"]
        }

    def errback_httpbin(self, failure):
        # log all failure
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exception come from HttpError spider middleware
            # get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is original request
            request = failure.request
            self.logger.error('DnsLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)