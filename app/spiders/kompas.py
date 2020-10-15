# -*- coding: utf-8 -*-
import scrapy


class KompasSpider(scrapy.Spider):
    name = "kompas"
    allowed_domains = ['news.kompas.com']
    start_urls = ['https://news.kompas.com/']


    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('div.article__grid > div.article__box'):
            title = quote.css('h3 > a::text').extract_first()
            if ("corona" or "covid" or "sars-cov-2") in title.lower():
                item = {
                    'status' : "found", 
                    'title': title,
                    'link': quote.css('h3 > a::attr(href)').extract_first(),
                    'date': quote.css('div.article__date::text').extract_first()
                }
                yield item
            else:
                item = {
                    'status' : "not found", 
                    'title': title,
                    'link': quote.css('h3 > a::attr(href)').extract_first(),
                    'date': quote.css('div.article__date::text').extract_first()
                }
                yield item
        # follow pagination link
        next_page_url = response.xpath("//a[contains(text(),'Next')]/@href").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
