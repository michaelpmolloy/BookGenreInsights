import scrapy
from scrapy.loader import ItemLoader
from goodreadsScraper.items import BookLinks


# run this by terminal command "scrapy crawl name" therefore "scrapy crawl goodreads"


#scrapy  with headers https://www.youtube.com/watch?v=UaqSo7hlX9g

class BookListSpider(scrapy.Spider):
    name = "bookListSpider"
    start_urls = ["https://www.goodreads.com/list/show/22", "https://www.goodreads.com/list/show/18", "https://www.goodreads.com/list/show/21", "https://www.goodreads.com/list/show/9", "https://www.goodreads.com/list/show/17", "https://www.goodreads.com/list/show/5", "https://www.goodreads.com/list/show/4093", "https://www.goodreads.com/list/show/143500"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

    def parse(self, response):

        for book in response.css('table.tableList.js-dataTooltip [itemtype="http://schema.org/Book"]'):
            l = ItemLoader(item=BookLinks(), selector=book)
            #l.add_css('authorLink', 'a.authorName::attr(href)')
            l.add_css('bookLink', 'a.bookTitle::attr(href)')
            yield l.load_item()

        next_page = response.css('a[rel=next]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
