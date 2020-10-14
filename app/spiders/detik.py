# -*- coding: utf-8 -*-
import scrapy


class DetikSpider(scrapy.Spider):
    name = "detik"
    allowed_domains = ['news.detik.com']
    start_urls = ['https://news.detik.com/indeks']


    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('article'):
            title = quote.css('div.media__text > h3.media__title > a::text').extract_first()
            if ("corona" or "covid" or "sars-cov-2") in title.lower():
                item = {
                    'status' : "found", 
                    'media__title': title,
                    'media__link': quote.css('div.media__text > h3.media__title > a::attr(href)').extract_first(),
                    'media__date': quote.css('div.media__text > div.media__date > span::attr(title)').extract_first()
                }
                yield item
            else:
                item = {
                    'status' : "not found", 
                    'media__title': title,
                    'media__link': quote.css('div.media__text > h3.media__title > a::attr(href)').extract_first(),
                    'media__date': quote.css('div.media__text > div.media__date > span::attr(title)').extract_first()
                }
                yield item
        # follow pagination link
        next_page_url = response.xpath("//a[contains(text(),'Next')]/@href").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)