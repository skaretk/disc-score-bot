#import json
#from collections import OrderedDict
from enum import Enum
import nextcord
from apis.discgolfmetrixapi import metrix_favicon

class DiscgolfmetrixCourseSource(Enum):
    """Discgolfmetric course source"""
    ID = 1
    LIST = 2

class DiscgolfmetrixCourse:
    """Discgolfmetrix Course"""
    def __init__(self, json, course_source:DiscgolfmetrixCourseSource):
        self.type = course_source
        self.course_json = json.get("course") if course_source == course_source.ID else json
        self.baskets_json = json.get("baskets") if course_source == course_source.ID else None
        self.course_url = f'https://discgolfmetrix.com/course/{self.course_id}'

    def calculate_rating(self, result = None):
        """Calculate and return course rating"""
        # rating values is only returned if searched by ID
        if self.type == DiscgolfmetrixCourseSource.LIST:
            return None
        if self.course_json is not None:
            rating_value_1 = self.course_json.get("RatingValue1")
            rating_result_1 = self.course_json.get("RatingResult1")
            rating_value_2 = self.course_json.get("RatingValue2")
            rating_result_2 = self.course_json.get("RatingResult2")
            if rating_value_1 and rating_result_1 and rating_value_2 and rating_result_2:
                rating_value_1 = float(rating_value_1)
                rating_result_1 = float(rating_result_1)
                rating_value_2 = float(rating_value_2)
                rating_result_2 = float(rating_result_2)
            else:
                return None

            if result is None:
                result = self.par
            if result is not None:
                return round( (rating_value_2 - rating_value_1) * (result - rating_result_1) / (rating_result_2 - rating_result_1) + rating_value_1 )
        return None

    @property
    def par(self):
        """Course par"""
        if self.baskets_json is not None:
            par = 0
            for hole in self.baskets_json:
                par += int(hole.get("Par"))
            return par
        return None

    @property
    def total_length(self):
        """Course total length"""
        if self.baskets_json is not None:
            length = 0
            for hole in self.baskets_json:
                if hole.get("Length") is not None:
                    length += (int)(hole.get("Length"))
            return length
        return None

    @property
    def no_of_baskets(self):
        """Number of baskets on the course"""
        if self.baskets_json is not None:
            return len(self.baskets_json)
        return None

    @property
    def course_name(self):
        """Course name"""
        if self.course_json is not None:
            return self.course_json.get("Fullname")
        return None

    @property
    def course_id(self):
        """Course id"""
        return self.course_json.get("ID")

    def get_embed(self):
        """Returns embed for discord"""
        description_text = ""
        try:
            description_text = f'Baskets: {self.no_of_baskets or "Unknown"} Par: {self.par or "0"} Length: {self.total_length or "0"}m PAR Rating: {self.calculate_rating() or "0"}'
        except:
            print("Could not fetch description for course")
        embed=nextcord.Embed(title=self.course_name, url=f'{self.course_url}', description=description_text, color=0x004899)
        embed.set_footer(text="discgolfmetrix", icon_url=metrix_favicon())
        return embed
