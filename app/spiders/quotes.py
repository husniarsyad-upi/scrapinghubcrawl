# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["detik.com"]
    start_urls = ['http://detik.com']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('article'):
            item = {
                'media__title': quote.css('a::text').extract_first(),
                'link': quote.css('a::attr(href)').extract_first(),
                'date': quote.css('span::attr(title)').extract_first(),
            }
            yield item
        # follow pagination link
        # next_page_url = response.css('li.next > a::attr(href)').extract_first()
        # if next_page_url:
        #     next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)