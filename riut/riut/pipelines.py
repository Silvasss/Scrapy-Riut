# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RiutPipeline:
    def process_item(self, item, spider):
        # Trata o dicionario que está sendo recebido da função principal, olha o código no git para ver como tratar baseado na versão anterior
        try:
            if item['Título:\xa0'] != None and item['Autor(es):\xa0'] != None and item['Orientador(es):\xa0'] != None and item['Palavras-chave:\xa0'] != None and item['Resumo:\xa0'] != None and item['URI:\xa0'] != None and item['Data do documento:\xa0'] != None:
                return {
                        "Título": item["Título:\xa0"],
                        "Autor(es)": item["Autor(es):\xa0"],
                        "Orientador(es)": item["Orientador(es):\xa0"],
                        "Palavras-chave": item["Palavras-chave:\xa0"],
                        "Data do documento": item["Data do documento:\xa0"],
                        "Resumo": item["Resumo:\xa0"],
                        "Repositorio": item["URI:\xa0"]
                    }
        except ValueError:
            return False

        #return True