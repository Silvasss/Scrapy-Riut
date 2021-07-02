import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from riut.items import RiutItem


#response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[3]/div/table//text()').extract() --- Retorna tudo sem os links
#response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[3]/div/table//a').extract() --- Retorna o nome da publicação e o link
#response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[3]/div/table//a/@href').extract() --- Retorna só o link da publicação
#response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[2]/ul/li[8]//a/@href').extract() --- Caminho para a próxima página


class ExampleSpider(scrapy.Spider):
    name = 'example'
    #https://repositorio.utfpr.edu.br/jspui/simple-search?query=saude+mental&sort_by=score&order=desc&rpp=100&etal=0&start=0
    start_urls = ['https://repositorio.utfpr.edu.br/jspui/simple-search?query=saude+mental']

    # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, callback = self.parse, errback = self.errback_httpbin, dont_filter = True)

    # Faz acontece, caso nao ocorra nenhum erro
    def parse(self, response):
        # Retorna os links das publicações
        links = response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[3]/div/table//a/@href').extract()

        for i in links:
            i = response.urljoin(i + '?model=full')

            yield scrapy.Request(i, callback = self.extracao)

        nextPage = response.xpath('//*[@id="content"]/div[3]/div/div[1]/div[2]/ul/li[8]//a/@href').extract()

        if nextPage:
            nextPage = response.urljoin(nextPage)

            yield scrapy.Request(nextPage, callback = self.parse)


    def extracao(self, response):
        itens = RiutItem()

        campos = response.xpath('.//*[@id="content"]/div[3]/table//tr')

        for i in campos:
            camp_chave = i.xpath('td[1]/text()').get()
            if camp_chave is not None:
                if 'Título' in i.xpath('td[1]/text()').get():
                    itens['Titulo'] = i.xpath('td[2]//text()').get()
                elif 'Autor(es)' in i.xpath('td[1]/text()').get():
                    itens['Autores'] = i.xpath('td[2]//text()').get()
                elif 'Orientador(es)' in i.xpath('td[1]/text()').get():
                    itens['Orientadores'] = i.xpath('td[2]//text()').get()
                elif 'Palavras-chave' in i.xpath('td[1]/text()').get():
                    itens['Palavraschaves'] = i.xpath('td[2]//text()').getall()
                elif 'Data do documento' in i.xpath('td[1]/text()').get():
                    itens['Datadocumento'] = i.xpath('td[2]//text()').get()
                elif 'Resumo' in i.xpath('td[1]/text()').get():
                    itens['Resumo'] = i.xpath('td[2]//text()').get()
                elif 'URI' in i.xpath('td[1]/text()').get():
                    itens['Repositorio'] = i.xpath('td[2]//text()').get()

        yield itens


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