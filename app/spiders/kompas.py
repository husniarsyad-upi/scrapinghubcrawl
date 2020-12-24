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
            cstats = 0
            
            if "corona" in title.lower():
                cstats = 1
            elif "covid" in title.lower():
                cstats = 1
            elif "sars-cov-2" in title.lower():
                cstats = 1

            if cstats == 1:
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
