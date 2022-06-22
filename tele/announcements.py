from datetime import datetime
from canvasapi import Canvas
from html2text import html2text
import pandas as pd
import pytz
from tele.constants import (
    CANVAS_DATE_FORMAT,
    IST,
    OUTPUT_DATE_FORMAT
)

class Announcements:
    
    def __init__(self,API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)
        self.announcements_df= pd.read_csv('csv/subscribers.csv',dtype='int64',error_bad_lines=False)

    def format_announcement(self,announcement,course):
        post_datetime = pytz.utc.localize(
            datetime.strptime(
                announcement.posted_at, CANVAS_DATE_FORMAT)
            ).astimezone(IST).strftime(OUTPUT_DATE_FORMAT)
        announcemnt_list = [] 
        announcemnt_list.append(f'*Recent announcement form {course.name}:* \n')
        title = announcement.title
        description = html2text(announcement.message)
        # print(announcement.message)
        announcemnt_list.append('\t<b>Title:<b>  {}\n\tTime:  {}\n\tDescription:  {}\n\t'
                                    .format(title, post_datetime,description))
        return announcemnt_list

    async def send_announcements(self,update, announcement):
        course_id = int(announcement.context_code[announcement.context_code.index("_")+1:])
        course = self.canvas.get_course(course_id)
        # ame= announcement.author['display_name'], url= announcement.url, icon_url= announcement.author['avatar_image_url'])
        # embed.set_footer(text=f'{post_datetime}\n{course.name}')
        formated_announcement = self.format_announcement(announcement,course)
        text_to_send = '\n'.join(formated_announcement)
        for index, row in self.announcements_df.iterrows():
                if row['Course_id'] == course_id: 
                    #send announcement to the chats/groups, only who have subscribed to this course.
                    await update.bot.send_message(chat_id=int(row['Chat_ID']), text= text_to_send)
    
    