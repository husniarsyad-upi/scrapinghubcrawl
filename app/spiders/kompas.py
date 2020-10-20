# -*- coding: utf-8 -*-
import scrapy
import re

class KompasSpider(scrapy.Spider):
    name = "kompas"
    allowed_domains = ['indeks.kompas.com']
    start_urls = ['https://indeks.kompas.com']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('div.article__list'):
            title = str(quote.css('div.article__list__title > h3 > a::text').extract_first().encode("utf-8"))
            if ("corona" or "covid" or "sars-cov-2") in title.lower():
                item = {
                    'status' : "found", 
                    'title': title,
                    'link': quote.css('div.article__list__title > h3 > a::attr(href)').extract_first(),
                    'date': quote.css('div.article__list__info > div.article__date::text').extract_first()
                }
                yield item
            else:
                item = {
                    'status' : "not found", 
                    'title': title,
                    'link': quote.css('div.article__list__title > h3 > a::attr(href)').extract_first(),
                    'date': quote.css('div.article__list__info > div.article__date::text').extract_first()
                }
                yield item
        # follow pagination link
        next_page_url = response.xpath("//a[contains(text(),'Next')]/@href").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
