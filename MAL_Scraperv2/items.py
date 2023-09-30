# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader
import re

class Anime(scrapy.Item):

    # Identification fields
    id = scrapy.Field()
    original_title = scrapy.Field()
    english_title = scrapy.Field()
    japanese_title = scrapy.Field()

    # Additional informations
    type = scrapy.Field()
    episodes_number = scrapy.Field()
    status = scrapy.Field()
    airing_date = scrapy.Field()
    premiered_date = scrapy.Field()
    broadcast_date = scrapy.Field()
    producers = scrapy.Field()
    licensors = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    genres = scrapy.Field()
    themes  = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    synopsis = scrapy.Field()

    opening_themes = scrapy.Field()
    ending_themes = scrapy.Field()
    pictures = scrapy.Field()




    #Statistics informations
    score = scrapy.Field()
    ranked = scrapy.Field()
    popularity = scrapy.Field()
    members = scrapy.Field()
    favorites = scrapy.Field()

class AnimeLoader(ItemLoader):
    default_output_processor = MapCompose(str.strip, lambda x:re.sub('\\n|\\r', '', x), lambda x:re.sub("\s{2,}", " ", x), lambda x:x.replace('"' ,"'"))

    airing_date_in = TakeFirst()
    broadcast_date_in = TakeFirst()
    duration_in = TakeFirst() 

    episodes_number_in = TakeFirst()
    favorites_in = TakeFirst()
    members_in = TakeFirst()
    popularity_in = TakeFirst()
    premiered_date_in = TakeFirst()
    ranked_in = TakeFirst()
    rating_in = TakeFirst()
    source_in = TakeFirst()
    status_in = TakeFirst()
    score_in = TakeFirst()
    opening_themes_in = Join()
    ending_themes_in = Join()

    synopsis_in = Join()
    type_in = TakeFirst()


class Reviews(scrapy.Item):
    author = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()

class Characters(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    surname = scrapy.Field()
    description = scrapy.Field()
    role_type = scrapy.Field()
    pictures = scrapy.Field()
    id_anime = scrapy.Field()

class VoiceActors(scrapy.Item):
    id = scrapy.Field()
    lang = scrapy.Field()
    name = scrapy.Field()
    surname = scrapy.Field()
    pictures = scrapy.Field()

class Staff(scrapy.Field):
    id = scrapy.Field()
    name = scrapy.Field()
    surname = scrapy.Field()
    roles = scrapy.Field()
    pictures = scrapy.Field()
    id_anime = scrapy.Field()