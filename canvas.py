import json
from turtle import update
from canvasapi import Canvas
import pytz

from tele.course_formatter import course_formatter
# import telebot
# import requests

# canvas_url = 'https://aheadonline.amrita.edu'
# canvas_api = 'yxDlbHuvnLUvX28wlbhtK9pu018QCz6pE2o0rrpXfWZG8tI2iyUfzp1B4SztRGr7'
IST = pytz.timezone('Asia/Kolkata')
CANVAS_DATE_FORMAT = r'%Y-%m-%dT%H:%M:%SZ'
OUTPUT_DATE_FORMAT = r'%a, %b %d at %I:%M %p'
API_KEY = '5460223513:AAFLCOuUnTAcX175NtPphOxss0Ghi7acYqo'  # telegram api
# bot = telebot.TeleBot(API_KEY)
# canvas_url = 'https://aheadonline.amrita.edu'
# canvas_api = 'yxDlbHuvnLUvX28wlbhtK9pu018QCz6pE2o0rrpXfWZG8tI2iyUfzp1B4SztRGr7'
# from dateutil import parser

class CanvasTele:
    """
    canvas_url: the url your institution uses to access canvas
    (e.g.) https://canvas.instructure.com
    """

    def __init__(self,canvas_url,canvas_api):
        self.canvas = Canvas(canvas_url,canvas_api)
        
    async def get_courses_list(self,update,context):
        print('hey!')
        courses = self.canvas.get_courses(enrollment_state="active")
        # print(courses[0])
        courses_texts = []
        courses_texts.append('List of all courses this sem\n')
        for course in courses:
            print(course)
        # courses_texts.append(course)
        # for course in courses:
        #     print(course)
        # text_to_send = '/n'.join(courses_texts)
        await update.message.reply_text('text_to_send')

    async def get_all_assingmets(self,update,context):
        print('assingmentsss!')
        courses = self.canvas.get_courses(enrollment_state="active")
        assingments = courses[1].get_assignments()
        print(assingments)
        await update.message.reply_text('yo! done')

# bot.polling()