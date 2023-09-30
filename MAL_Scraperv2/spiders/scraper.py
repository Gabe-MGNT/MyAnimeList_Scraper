from collections import OrderedDict, Counter

import scrapy
import string
import re

from ..items import Anime, AnimeLoader, Reviews, Characters, VoiceActors, Staff
from scrapy.loader import ItemLoader


class AnimeScraper(scrapy.Spider):
    name="AnimeScraper"

    start_urls = [
        "https://myanimelist.net/anime/1"
    ]

    def parse(self,response):
        for id_number in range(1,70000):
            url_to_parse = f"https://myanimelist.net/anime/{id_number}"
            yield scrapy.Request(url = url_to_parse, callback = self.parse_anime_page)
            return

    def parse_anime_page(self, response):

        anime_entity = AnimeLoader(item=Anime(), response=response)
        anime_entity.add_css("original_title", 'h1 ::text')
        anime_entity.add_xpath("japanese_title", "//*[starts-with(text(),'Japanese:')]/following-sibling::text()")
        anime_entity.add_xpath("english_title", "//*[starts-with(text(),'English:')]/following-sibling::text()")
        anime_entity.add_xpath("type", "//*[starts-with(text(),'Type:')]/following-sibling::*/text()")
        anime_entity.add_xpath("episodes_number", "//*[starts-with(text(),'Episodes:')]/following-sibling::text()")
        anime_entity.add_xpath("status", "//div/*[starts-with(text(),'Status:')]/following-sibling::text()")
        anime_entity.add_xpath("airing_date", "//div/*[starts-with(text(),'Aired:')]/following-sibling::text()")
        anime_entity.add_xpath("premiered_date", "//div/*[starts-with(text(),'Premiered:')]/following-sibling::*/text()")
        anime_entity.add_xpath("broadcast_date", "//div/*[starts-with(text(),'Broadcast:')]/following-sibling::text()")
        anime_entity.add_xpath("producers", "//div/*[starts-with(text(),'Producers:')]/following-sibling::*//text()")
        anime_entity.add_xpath("licensors", "//div/*[starts-with(text(),'Licensors:')]/following-sibling::*/text()")
        anime_entity.add_xpath("studios", "//div/*[starts-with(text(),'Studios:')]/following-sibling::*/text()")
        anime_entity.add_xpath("source", "//div/*[starts-with(text(),'Source:')]/following-sibling::text()")
        anime_entity.add_xpath("genres", "//div/*[starts-with(text(),'Genres:')]/following-sibling::*/text()")
        anime_entity.add_xpath("themes", "//div/*[starts-with(text(),'Theme:')]/following-sibling::*/text()")
        anime_entity.add_xpath("duration", "//div/*[starts-with(text(),'Duration:')]/following-sibling::text()")
        anime_entity.add_xpath("rating", "//div/*[starts-with(text(),'Rating:')]/following-sibling::text()")
        anime_entity.add_xpath("synopsis", "//div[h2[contains(.,'Synopsis')]]/following-sibling::p//text()")
        anime_entity.add_xpath("score", "//div/*[starts-with(text(),'Score:')]/following-sibling::*/text()")
        anime_entity.add_xpath("ranked", "//div/*[starts-with(text(),'Ranked:')]/following-sibling::*/text()")
        anime_entity.add_xpath("popularity", "//div/*[starts-with(text(),'Popularity:')]/following-sibling::text()")
        anime_entity.add_xpath("members", "//div/*[starts-with(text(),'Members:')]/following-sibling::text()")
        anime_entity.add_xpath("favorites", "//div/*[starts-with(text(),'Favorites:')]/following-sibling::text()")


        endings = response.xpath("//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr")
        for ending in range(len(endings)):
            anime_entity.add_xpath("ending_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{ending}]//span//text()")
        
        openings = response.xpath("//div[h2[contains(.,'Opening Theme')]]/following-sibling::*//tr")
        for opening in range(len(openings)):
            anime_entity.add_xpath("opening_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{opening}]//span//text()")
        
        return anime_entity.load_item()

        """
        title = response.css('h1 ::text').get()
        japanese_name = response.xpath("//*[starts-with(text(),'Japanese:')]/following-sibling::text()").get()
        english_name = response.xpath("//*[starts-with(text(),'English:')]/following-sibling::text()").get()
        type = response.xpath("//*[starts-with(text(),'Type:')]/following-sibling::*/text()").get()
        episodes = response.xpath("//*[starts-with(text(),'Episodes:')]/following-sibling::text()").get()
        status = response.xpath("//div/*[starts-with(text(),'Status:')]/following-sibling::text()").get()
        aired_date = response.xpath("//div/*[starts-with(text(),'Aired:')]/following-sibling::text()").get()
        premiered = response.xpath("//div/*[starts-with(text(),'Premiered:')]/following-sibling::*/text()").get()
        broadcast = response.xpath("//div/*[starts-with(text(),'Broadcast:')]/following-sibling::text()").get()
        previewed = response.xpath("//div/*[starts-with(text(),'Previewed:')]/following-sibling::text()").get()
        source = response.xpath("//div/*[starts-with(text(),'Source:')]/following-sibling::text()").get()
        duration = response.xpath("//div/*[starts-with(text(),'Duration:')]/following-sibling::text()").get()
        rating = response.xpath("//div/*[starts-with(text(),'Rating:')]/following-sibling::text()").get()

        score = response.xpath("//div/*[starts-with(text(),'Score:')]/following-sibling::*/text()").get()
        ranked = response.xpath("//div/*[starts-with(text(),'Ranked:')]/following-sibling::*/text()").get()
        popularity = response.xpath("//div/*[starts-with(text(),'Popularity:')]/following-sibling::text()").get()
        members = response.xpath("//div/*[starts-with(text(),'Members:')]/following-sibling::text()").get()
        favorites = response.xpath("//div/*[starts-with(text(),'Favorites:')]/following-sibling::text()").get()



        # List
        producers = response.xpath("//div/*[starts-with(text(),'Producers:')]/following-sibling::*//text()").getall()
        licensors = response.xpath("//div/*[starts-with(text(),'Licensors:')]/following-sibling::*/text()").getall()
        studios = response.xpath("//div/*[starts-with(text(),'Studios:')]/following-sibling::*/text()").getall()
        
        # Maybe take summary on anidb
        anidb_link = response.xpath("//a[contains(@href,'anidb')]/@href").get()
        summary = response.xpath("//div[h2[contains(.,'Synopsis')]]/following-sibling::p//text()").getall()
        
        # RM Duplicates (List)
        genres = response.xpath("//div/*[starts-with(text(),'Genres:')]/following-sibling::*/text()").getall()
        
        # maybe take theme from animenews
        themes = response.xpath("//div/*[starts-with(text(),'Theme:')]/following-sibling::*/text()").getall()
        animenews_link = response.xpath("//a[contains(@href,'animenews')]/@href").get()
        """
