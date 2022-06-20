# from calendar import calendar
from datetime import datetime
from canvasapi import Canvas
from click import pass_context
from tele.announcements import Announcement
from tele.assignments import Assignments
from tele.constants import IST
from tele.constants import(
    CANVAS_URL,
    CANVAS_TOKEN,
)

course_ids = []
announcements_client = Announcement(CANVAS_URL, CANVAS_TOKEN)


class CanvasTele:

    def __init__(self, API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)
        self.assignment = Assignments(API_URL, CANVAS_TOKEN)
        self.last_check_time = datetime.now()
        print(self.courses_list())

    # fill the course_ids[] with currently enrolled active courses in canvas LMS
    def courses_list(self):
        courses = self.canvas.get_courses(enrollment_state="active")
        for course in courses:
            course_ids.append(course.id)
        return course_ids
    
    def course_formatter(self):
        list_of_courses =[]
        title = "Available courses"
        description = "Here are all of the courses this bot has access to along with their corresponding codes"
        # print(announcement.message)
        list_of_courses.append("\tTitle:  {}\nDescription:  {}\n\t"
                                    .format(title,description))
        courses = self.canvas.get_courses(enrollment_state="active")
        for course in courses:
            list_of_courses.append(f'{course.name} ({course.id})')
        return list_of_courses
    
    async def get_courses_list(self,update,context):
        formated_courses = self.course_formatter()    
        text_to_send = '\n'.join(formated_courses)
        await update.message.reply_text(text_to_send)
        
        
    async def get_assingment(self, update, context):
        current_datetime = datetime.now().astimezone(IST)
        msg = update.message['text']
        # remove the command, '/due', from the string and get the course id give by user
        course_id = msg[4:].strip()
        # print(course_id)
        if course_id == '':
            await self.get_all_assignments(update, context)
        else:
            try:
                # convert the message/course id to int
                course_id = int(course_id)
                # and check if it is a valid course id which is present in int list
                if course_ids.count(course_id) != 0:
                    await self.assignment.send_reminder(update, course_id, current_datetime)
                else:
                    await update.message.reply_text("Please enter a valid course id :)")
            except:  # message is not type int...
                return await update.message.reply_text("Please enter a valid integer value :)")

     # send all the due assingments for every subject

    async def get_all_assignments(self, update, context):
        current_datetime = datetime.now().astimezone(IST)
        # time = current_datetime.strftime("%H:%M")
        for course in course_ids:
            await self.assignment.send_reminder(update, course, current_datetime)

    async def get_annoucements(self, update):
        current_datetime = datetime.now().astimezone(IST)
        print(f'current time: {current_datetime}')
        print(f'last check time: {self.last_check_time}')
        # time = current_datetime.strftime("%H:%M")
        announcements = announcements_client.canvas.get_announcements(
            context_codes=course_ids, start_date=self.last_check_time, end_date=current_datetime)
        for announcement in announcements:
            print(f'Sending {announcement}')
            await announcements_client.send_announcements(update, announcement)
        # update last check time to current date and time
        self.last_check_time = current_datetime

    # async def calender_events(self,update,context):
    #     calender_event = self.canvas.get_calendar_events()
    #     events = []
    #     print(calender_event[0])
    #     for c in range(0,len(list(calender_event))):
    #             events.append(calender_event[c].__str__())
    #     text_to_send = '\n '.join(events)
    #     await update.message.reply_text(text_to_send)
