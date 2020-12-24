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
            cstats = 0
            
            if "corona" in title.lower():
                cstats = 1
            else if "covid" in title.lower():
                cstats = 1
            else if "sars-cov-2" in title.lower():
                cstats = 1

            if cstats == 1:
                item = {
                    'status' : "found", 
                    'title': title,
                    'link': quote.css('div.media__text > h3.media__title > a::attr(href)').extract_first(),
                    'date': quote.css('div.media__text > div.media__date > span::attr(title)').extract_first()
                }
                yield item
            else:
                item = {
                    'status' : "not found", 
                    'title': title,
                    'link': quote.css('div.media__text > h3.media__title > a::attr(href)').extract_first(),
                    'date': quote.css('div.media__text > div.media__date > span::attr(title)').extract_first()
                }
                yield item
        # follow pagination link
        next_page_url = response.xpath("//a[contains(text(),'Next')]/@href").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
