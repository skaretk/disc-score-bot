import nextcord
from apis.discgolfmetrixapi import metrix_favicon


class MetrixCourses:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def format_courses_description(self):
        description_text = ''
        for course in self.courses:
            description_text += f'\n[{course.course_name}]({course.course_url})'
        return description_text

    def get_embed(self):
        embed=nextcord.Embed(title=f'Found {len(self.courses)} {"Course" if len(self.courses) == 1 else "Courses"}', description=f'{self.format_courses_description()}', color=0x004899)
        embed.set_footer(text="discgolfmetrix", icon_url=metrix_favicon())
        return embed