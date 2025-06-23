# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#Input and output processors explained: https://stackoverflow.com/questions/54924697/how-should-i-choose-input-processor-and-output-processor-in-scrapy-i-dont-see

import scrapy
import re
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from dateutil.parser import parse as datautil_parse


def full_link(response):
    base_url = "https://www.goodreads.com"
    return base_url + response

def extract_number(response):
    #return ''.join(filter(str.isdigit, response))
    return re.findall(r"\d+", response) #returns first number from list

def remove_commas(response):
    return response.replace(',', '')


def convert_time(response):
    date_obj = datautil_parse(response, fuzzy=True).date()  #datautil_parse returns datetime object then date is extracted
    date_string = date_obj.strftime('%Y-%m-%d')
    return date_string


class BookLinks(scrapy.Item):
    #authorLink = scrapy.Field(input_process=remove_tags, output_processor=TakeFirst())
    bookLink = scrapy.Field(input_processor=MapCompose(full_link))

#input processor is applied to everything loaded into item variable, output processor is only applied to the output of the input process
#Mapcomopse as an output process returns list instead of string value therefore should only be used in output process when list is wanted
#usually when returning list it is because I fed in a list into map compose therefor making a list of lists.
#Takefirst therefore takes the first item in the mapcompose list which is still a list

class Book(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    avgRating = scrapy.Field(input_processor = lambda x: str(x[0]), output_processor = TakeFirst())
    numRatings = scrapy.Field(input_processor=MapCompose(remove_commas), output_processor=TakeFirst())
    numReviews = scrapy.Field(input_processor=MapCompose(remove_commas), output_processor=TakeFirst())
    publishDate = scrapy.Field(output_processor=TakeFirst())
    numPages = scrapy.Field(input_processor=lambda x: extract_number(str(x[0])), output_processor=TakeFirst())
    genreOne = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor= lambda x: x[0])
    genreTwo = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=lambda x: x[1])
    genreThree = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=lambda x: x[2])