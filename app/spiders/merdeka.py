# -*- coding: utf-8 -*-
import scrapy


class MerdekaSpider(scrapy.Spider):
    name = "merdeka"
    allowed_domains = ['m.merdeka.com']
    start_urls = ['https://m.merdeka.com/berita-hari-ini']


    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('div#mdk-news-list_m > ul > li'):
            title = quote.css('a::text').extract_first().strip()
            cstats = 0

            if "corona" in title.lower():
                cstats = 1
            elif "covid" in title.lower():
                cstats = 1
            elif "sars-cov-2" in title.lower():
                cstats = 1

            news_url = quote.css('a::attr(href)').extract_first()
            if cstats == 1:
                item = {
                    'status' : "found", 
                    'title': title,
                    'link': response.urljoin(news_url),
                    'date': quote.css('b.mdk-time::text').extract_first()
                }
                yield item
            else:
                item = {
                    'status' : "not found", 
                    'title': title,
                    'link': response.urljoin(news_url),
                    'date': quote.css('b.mdk-time::text').extract_first()
                }
                yield item
        # follow pagination link
        next_page_url = response.css('a.link_next::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
