from asyncio import events
from calendar import calendar
from datetime import datetime
from canvasapi import Canvas
from telegram import Update
from telegram.ext import CallbackContext
from tele.announcements import Announcement
from tele.assignments import Assignments

from tele.constants import CANVAS_DATE_FORMAT, IST, OUTPUT_DATE_FORMAT
from tele.course_formatter import course_formatter
from tele.constants import(
    CANVAS_URL,
    CANVAS_TOKEN,
    API_KEY
)

course_ids = []
announcements_cmd = Announcement(CANVAS_URL,CANVAS_TOKEN)
class CanvasTele:

    def __init__(self, API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)
        
        self.assignment = Assignments(API_URL,CANVAS_TOKEN)
        self.last_check_time = datetime.now()
        self.get_courses_list()
        
     

    def get_courses_list(self):
        print('list of active course names')
        courses = self.canvas.get_courses(enrollment_state="active")
        
        for course in courses:
            course_ids.append(course.id)
        # text_to_send = '\n '.join(course_names)
        return course_ids
            
    async def get_assingment(self,update,context):
        current_datetime = datetime.now().astimezone(IST)
        msg = update.message['text']   
        course_id = msg[4:].strip()
        print(course_id)
        if course_id == '':
            await self.get_all_assingmets(update,context)  
        else:
            try:
                course_id = int(course_id)
                if course_ids.count(course_id) != 0 :
                    await self.assignment.send_reminder(update, course_id, current_datetime)            
                else:
                    await update.message.reply_text("Please enter a valid course id :)")
            except:
                return await update.message.reply_text("Please enter a valid integer value :)")
               
            
           
    async def get_all_assingmets(self, update,context):
        current_datetime = datetime.now().astimezone(IST)
        # time = current_datetime.strftime("%H:%M")
        for course in course_ids:
            await self.assignment.send_reminder(update, course, current_datetime)
    
    async def get_annoucements(self,update):
        current_datetime = datetime.now().astimezone(IST)
        print(current_datetime)
        # time = current_datetime.strftime("%H:%M")
        # courses_list = [course.id for course in courses]
        # print(self.last_check_time)
        # print(current_datetime)
        announcements = announcements_cmd.canvas.get_announcements(context_codes = course_ids,end_date = current_datetime)
        #start_date = self.last_check_time,
        for announcement in announcements:
            print(f'Sending {announcement}')
            # print(announcement.context_code)
            await announcements_cmd.send_announcements(update,announcement)
        
        # self.last_check_time = current_datetime

    # async def calender_events(self,update,context):
    #     calender_event = self.canvas.get_calendar_events()
    #     events = []
    #     print(calender_event[0])
    #     for c in range(0,len(list(calender_event))):
    #             events.append(calender_event[c].__str__())
    #     text_to_send = '\n '.join(events)
    #     await update.message.reply_text(text_to_send)


# bot.polling()
