from asyncio import events
from calendar import calendar
from datetime import datetime
import json
from msilib import text
from turtle import update
from canvasapi import Canvas
import canvasapi
import pandas as pd
import pytz

from tele.constants import CANVAS_DATE_FORMAT, IST, OUTPUT_DATE_FORMAT
from tele.course_formatter import course_formatter


class CanvasTele:

    def __init__(self, API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)

    async def get_courses_list(self, update, context):
        print('list of active course names')
        courses = self.canvas.get_courses(enrollment_state="active")
        course_names = []
        for course in courses:
            course_names.append(course.name)
        text_to_send = '\n '.join(course_names)
        await update.message.reply_text(text_to_send)

    def get_assignment_formatted(self,course,assignments_list,due_date_list):
        assignments_texts = []
        assignments_texts.append(f'Assignments dues for {course}: \n')
        for x in range(0,len(assignments_list)):
            title = assignments_list[x]
            last_date = due_date_list[x]
        # post time is in UTC because canvas returns a timestamp in UTC
        # the telegram api doesn't seem to support retrieving a timezone for a user
        # the canvas api supports this, so that can be used to format this timezone
        # a Course object contains timezone data, and announcements are tied to a course
            assignments_texts.append('Title:  {}\n\tTime:  {}\n\t'
                                    .format(title, last_date))
        # print(assignments_texts)
        return assignments_texts

    async def send_reminder(self, update, course_id, today):
        chat_id = int(update.message.chat_id)
        course = self.canvas.get_course(int(course_id))
        due_today = []
        for assignment in course.get_assignments():
            if assignment.due_at:
                due_date = pytz.utc.localize(datetime.strptime(
                    assignment.due_at, CANVAS_DATE_FORMAT)).astimezone(IST)
                if due_date.day == today.day and due_date.month == today.month and due_date.year == today.year:
                    due_today.append((assignment, due_date))

        assignments_list = []
        due_date_list = []
        for assignment, due_date in sorted(due_today, key=lambda a: a[1]):
            assignments_list.append(assignment.name)
            due_date_list.append(due_date.strftime(OUTPUT_DATE_FORMAT))

        if len(due_today) == 0:
            print(f"no assignments reminder for {course.name} today :)")
            return  # If there aren't any assignments due today, don't send a reminder
        # for x in assignments_list:
        print(len(assignments_list))
        formatted_assignments = self.get_assignment_formatted(course.name,assignments_list ,due_date_list)
        # for elem in formatted_assignments:
        text_to_send = '\n'.join(formatted_assignments)
        await update.message.reply_text(text_to_send)

    async def get_all_assingmets(self, update, context):
        print('assingmentsss!')
        current_datetime = datetime.now().astimezone(IST)
        time = current_datetime.strftime("%H:%M")
        courses = self.canvas.get_courses(enrollment_state="active")
        for course in courses:
            await self.send_reminder(update, course.id, current_datetime)
        
        
        
        # list_of_assingments = []
        # for i in range(0,len(list(courses))):
        #     ass = courses[i].get_assignments()
        #     print(ass.name , ass.id)
        # print(list_of_assingments)
        # await update.message.reply_text(update.message.chat_id)

    # async def calender_events(self,update,context):
    #     calender_event = self.canvas.get_calendar_events()
    #     events = []
    #     print(calender_event[0])
    #     for c in range(0,len(list(calender_event))):
    #             events.append(calender_event[c].__str__())
    #     text_to_send = '\n '.join(events)
    #     await update.message.reply_text(text_to_send)


# bot.polling()
