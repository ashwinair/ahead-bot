from datetime import datetime
from canvasapi import Canvas
from html2text import html2text
from telegram.constants import ParseMode
import pytz
from tele.constants import (
    CANVAS_DATE_FORMAT,
    IST,
    OUTPUT_DATE_FORMAT
)

class Announcement:
    
    def __init__(self,API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)
        

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
        await update.bot.send_message(chat_id=604663713, text= text_to_send)


# async def add_announcement(self, ctx, course_id):
    
#         course = self.canvas.get_course(course_id)
#         self.announcement_df = self.announcement_df.append(pd.DataFrame(
#             [[ctx.channel.id, course_id]], columns=self.announcement_df.columns), ignore_index=True)
#         embed = discord.Embed(
#             title='Successfully subscribed to course announcements',
#             description=f'This channel will now automatically recieve announcements from Canvas for the specified course. To unsubscribe, use the remove_announcement command'
#         )
#         embed.add_field(name='Course ID', value=course_id)
#         embed.add_field(name='Course name', value=course.name)
#         await ctx.send(embed=embed)
#         self.announcement_df.to_csv('csv/Announcements.csv', index=False)

# #     async def remove_announcement(self, ctx, course_id):  
# #         channel_announcements = self.announcement_df[self.announcement_df["Channel_ID"] == ctx.channel.id]
# #         to_be_deleted = channel_announcements[channel_announcements["Course_ID"] == course_id]
# #         self.announcement_df = self.announcement_df.drop(
# #             to_be_deleted.index.tolist())
# #         embed = discord.Embed(
# #             title='Successfully removed Canvas announcement subscription',
# #             description=f'This channel will no longer automatically recieve announcements from Canvas for:\n{self.canvas.get_course(course_id)}'
# #         )
# #         await ctx.send(embed=embed)
# #         self.announcement_df.to_csv('csv/Announcements.csv', index=False)
        
# #     # def get_announcements_formatted(announcements):
# #     #     announcement_texts = []
# #     #     announcement_texts.append('Recent announcements\n')
# #     #     for announcement in announcements:
# #     #         title = announcement['title']
# #     #         author = announcement['author']['display_name']
# #     #         course = announcement['course_name']
# #     #     # post time is in UTC because canvas returns a timestamp in UTC
# #     #     # the telegram api doesn't seem to support retrieving a timezone for a user
# #     #     # the canvas api supports this, so that can be used to format this timezone
# #     #     # a Course object contains timezone data, and announcements are tied to a course
# #     #         post_time = parser.parse(announcement['posted_at']).ctime()
# #     #         message = strip_tags(announcement['message'])
# #     #         announcement_texts.append('Title: {}\n\tCourse: {}\n\tAuthor: {}\n\tTime (UTC): {}\n\tMessage: {}\n'
# #     #             .format(title, course, author, post_time, message))
# #     #     return announcement_texts
    
    