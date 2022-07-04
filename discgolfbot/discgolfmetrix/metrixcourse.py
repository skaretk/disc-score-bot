#import json
#from collections import OrderedDict
from enum import Enum
import nextcord
from apis.discgolfmetrixapi import metrix_favicon

class MetrixCourseType(Enum):
    ID = 1
    LIST = 2

class MetrixCourse:
    def __init__(self, json, type: MetrixCourseType):
        self.type = type
        self.course_json = json.get("course") if type == type.ID else json
        self.baskets_json = json.get("baskets") if type == type.ID else None

    def calculate_rating(self, result = None):
        # rating values is only returned if searched by ID
        if self.type == MetrixCourseType.LIST:
            return None
        if self.course_json is not None:
            rating_value_1 = None
            rating_result_1 = None
            rating_value_2 = None
            rating_result_2 = None
            try:
                rating_value_1 = float(self.course_json.get("RatingValue1"))
                rating_result_1 = float(self.course_json.get("RatingResult1"))
                rating_value_2 = float(self.course_json.get("RatingValue2"))
                rating_result_2 = float(self.course_json.get("RatingResult2"))
            except:
                return None
            if result is None:
                result = self.get_par()
            if result is not None:
                return (rating_value_2 - rating_value_1)*(result - rating_result_1)/(rating_result_2 - rating_result_1)+rating_value_1
        return None

    def get_par(self):
        if self.baskets_json is not None:
            par = 0
            for hole in self.baskets_json:
                par += int(hole.get("Par"))
            return par
        return None

    def get_length(self):
        if self.baskets_json is not None:
            length = 0
            for hole in self.baskets_json:
                if hole.get("Length") != None:
                    length += (int)(hole.get("Length"))
            return length
        return None

    def get_basket_no(self):
        if self.baskets_json is not None:
           return len(self.baskets_json)
        return None

    def get_course_name(self):
        if self.course_json is not None:
            return self.course_json.get("Fullname")
        return None

    def get_course_id(self):
        if self.course_json is not None:
            return self.course_json.get("ID")
        return None

    def get_course_url(self):
        if self.course_json is not None:
            return f'https://discgolfmetrix.com/course/{self.course_json.get("ID")}'
        return None

    def get_embed(self):
        description_text = ""
        try:
            description_text = f'Baskets: {self.get_basket_no()} Par: {self.get_par()} Length:{self.get_length()}m PAR Rating: {round(self.calculate_rating(), 2)}'
        except:
            print("Could not fetch description for course")
        embed=nextcord.Embed(title=self.get_course_name(), url=f'{self.get_course_url()}', description=description_text, color=0x004899)
        embed.set_footer(text="discgolfmetrix", icon_url=metrix_favicon())
        return embed
