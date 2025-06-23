import scrapy
from scrapy.loader import ItemLoader
from goodreadsScraper.items import Book
from goodreadsScraper.items import convert_time

#How to use: scrapy crawl bookSpider -a filename=text.txt


class BookSpider(scrapy.Spider):
    name = 'bookSpider'

    custom_settings = {
        'ITEM_PIPELINES': {
            "goodreadsScraper.pipelines.DuplicateBookPipeline" : 200,
            "goodreadsScraper.pipelines.MysqlDatabasePipeline": 300
        }
    }

    with open('/Users/michaelmolloy/Code/goodreadsScrape/goodreadsScraper/allBookLinks.csv', 'rt') as f:
        start_urls = [url.strip() for url in f.readlines()[1:]]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

    def parse(self, response):
        l = ItemLoader(item = Book(), response=response)
        l.add_css('title', 'h1::text')
        l.add_css('author', 'span.ContributorLink__name::text')
        l.add_value('avgRating', response.css('div.RatingStatistics__rating::text'))
        l.add_value('numPages', response.css('p[data-testid="pagesFormat"]::text'))
        l.add_css('numRatings', 'span[data-testid="ratingsCount"]::text')
        l.add_css('numReviews', 'span[data-testid="reviewsCount"]::text')
        l.add_value('publishDate', convert_time(response.css('p[data-testid="publicationInfo"]::text').extract()[0]))
        l.add_css('genreOne', 'span.BookPageMetadataSection__genreButton span.Button__labelItem::text')
        l.add_css('genreTwo', 'span.BookPageMetadataSection__genreButton span.Button__labelItem::text')
        l.add_css('genreThree', 'span.BookPageMetadataSection__genreButton span.Button__labelItem::text')
        #add_value used in cases where add_css was returning list instead of string
        yield l.load_item()




