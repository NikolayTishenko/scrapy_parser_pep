import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('td a[href^="pep-"]')
        for pep in all_peps:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_info = response.css('h1.page-title::text').get()
        number = pep_info.split(' ')[1]
        name = pep_info.split(' – ')[1]
        data = {
            'number': number,
            'name': name,
            'status': response.css('abbr::text').get()
        }
        yield PepParseItem(data)
