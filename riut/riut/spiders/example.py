import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ExampleSpider(scrapy.Spider):
    name = 'example'

    start_urls = []

    # Criando os links dos repositorios
    for i in range(0, 23500):
        start_urls.append("https://repositorio.utfpr.edu.br/jspui/handle/1/{}".format(i))

    # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, callback = self.parse, errback = self.errback_httpbin, dont_filter = True)

    # Faz acontece, caso nao ocorra nenhum erro
    def parse(self, response):
        # Dicionario temporario
        dictAux = {}

        for post in response.css("tr"):

            dictAux[post.css("::text")[0].get()] = post.css("::text")[1].get()

        yield dictAux


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