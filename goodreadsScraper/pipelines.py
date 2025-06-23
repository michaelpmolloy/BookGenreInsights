# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import mysql.connector

from scrapy.exceptions import DropItem

#class GoodreadsscraperPipeline:
#    def process_item(self, item, spider):
#        return item


#class DuplicateLinkPipeline(object):
#    def __init__(self):
#        self.item_seen = set()
#
#    def process_item(self, item, spider):
#        item_key  = item['bookLink']
#        if item_key in self.item_seen:
#            raise DropItem("Duplicate item: %s" % item)
#        else:
#            self.item_seen.add(item_key)
#            return item



class DuplicateBookPipeline(object):
    def __init__(self):
        self.item_seen = set()

    def process_item(self, item, spider):
        item_key  = (item['title'], item['author'])
        if item_key in self.item_seen:
            raise DropItem("Duplicate item: %s" % item)
        else:
            self.item_seen.add(item_key)
            return item


class MysqlDatabasePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'ultra45moss$',
            database = 'goodreadsBooks'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS books_tb""")
        self.curr.execute("""CREATE TABLE books_tb(
            title VARCHAR(255),
            author VARCHAR(255),
            avgRating FLOAT,
            numRatings INT,
            numReviews INT,
            publishDate DATE,
            numPages INT,
            genreOne VARCHAR(255),
            genreTwo VARCHAR(255),
            genreThree VARCHAR(255)
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):

        #for key, value in item.items():
        #    print(f"The data type of '{key}' is: {type(value)}")

        self.curr.execute("""INSERT INTO books_tb (title, author, avgRating, numRatings, numReviews, publishDate, numPages, genreOne, genreTwo, genreThree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            item['title'],
            item['author'],
            item['avgRating'],
            item['numRatings'],
            item['numReviews'],
            item['publishDate'],
            item['numPages'],
            item['genreOne'],
            item['genreTwo'],
            item['genreThree']
        ))


        self.conn.commit()




