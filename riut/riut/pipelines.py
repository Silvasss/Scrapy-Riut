# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from datetime import datetime

class RiutPipeline:
    def process_item(self, item, spider):
        datas = {0o1: 'Jan', 0o2: 'Fev', 0o3: 'Mar', 0o4: 'Abri', 0o5: 'Mai', 0o6: 'Jun', 0o7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}

        if len(item) != 7:
            item = {}
        else:
            #
            aux = item['Datadocumento'].split('-')

            for i in datas:
                try:
                    if datas[i] == aux[1]:
                        item['Datadocumento'] = f"{aux[0]}-{i}-{aux[2]}"
                except ValueError:
                    pass

        return item