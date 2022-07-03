import json
from collections import OrderedDict
import nextcord
from apis.discgolfmetrixapi import metrix_favicon, metrix_logo

class MetrixCourse:
    def __init__(self, json):
        self.json = json
        self.course_url = 'https://discgolfmetrix.com/course'

    def calculate_rating(self, result = None):
        if self.json is not None:
            course = self.json.get("course")
            rating_value_1 = None
            rating_result_1 = None
            rating_value_2 = None
            rating_result_2 = None
            try:
                rating_value_1 = float(course.get("RatingValue1"))
                rating_result_1 = float(course.get("RatingResult1"))
                rating_value_2 = float(course.get("RatingValue2"))
                rating_result_2 = float(course.get("RatingResult2"))
            except:
                return None
            if result is None:
                result = self.get_par()
            if result is not None:
                return (rating_value_2 - rating_value_1)*(result - rating_result_1)/(rating_result_2 - rating_result_1)+rating_value_1
        return None

    def get_par(self):
        if self.json is not None:
            baskets = self.json.get("baskets")
            if baskets is not None:
                par = 0
                for hole in baskets:
                    par += int(hole.get("Par"))
                return par
        return None

    def get_length(self):
        if self.json is not None:
            baskets = self.json.get("baskets")
            if baskets is not None:
                length = 0
                for hole in baskets:
                    if hole.get("Length") != None:
                        length += (int)(hole.get("Length"))
                return length
        return None

    def get_basket_no(self):
        if self.json is not None:
            baskets = self.json.get("baskets")
            if baskets is not None:
                return len(baskets)
        return None

    def get_course_name(self):
        if self.json is not None:
            course = self.json.get("course")
            return course.get("Fullname")
        return None

    def get_course_id(self):
        if self.json is not None:
            course = self.json.get("course")
            return course.get("ID")
        return None

    def get_embed(self):
        description_text = ""
        try:
            description_text = f'Baskets: {self.get_basket_no()} Par: {self.get_par()} Length:{self.get_length()}m PAR Rating: {round(self.calculate_rating(), 2)}'
        except:
            print("Could not fetch description for course")
        embed=nextcord.Embed(title=self.get_course_name(), url=f'{self.course_url}/{self.get_course_id()}', description=description_text, color=0x004899)
        embed.set_footer(text="discgolfmetrix api", icon_url=metrix_favicon())
        #embed.set_thumbnail(url=metrix_logo())
        return embed
