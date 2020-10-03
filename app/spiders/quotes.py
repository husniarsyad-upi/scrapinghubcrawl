# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["news.detik.com/indeks"]
    start_urls = ['https://news.detik.com/indeks']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('article'):
            item = {
                'media__title': quote.css('div.media__text > h3.media__title > a::text').extract_first(),
                'media__link': quote.css('div.media__text > h3.media__title > a::attr(href)').extract_first(),
                'media__date': quote.css('div.media__text > div.media__date > span::attr(title)').extract_first(),
            }
            yield item
        # follow pagination link
        next_page_url = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)