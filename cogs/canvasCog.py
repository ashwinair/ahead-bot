import discord
from discord import Client
from discord.ext import commands, tasks
from canvasapi import Canvas
import datetime
import pytz
from time import perf_counter
import pandas as pd
from html2text import html2text
from config import CANVAS_TOKEN

API_URL = 'https://aheadonline.amrita.edu/login/canvas'
IST = pytz.timezone('Asia/Kolkata')
CANVAS_DATE_FORMAT = r'%Y-%m-%dT%H:%M:%SZ'
OUTPUT_DATE_FORMAT = r'%a, %b %d at %I:%M %p'


class CanvasCog(commands.Cog):
    def __init__(self,bot):
        self.bot= bot
        self.canvas = Canvas(API_URL,CANVAS_TOKEN)
        self.announcements_df= pd.read_csv('csv/Announcements.csv',dtype='int64')


    def cog_unload(self):
        print("Unloading Canvas Cog")
        self.clock.cancel()
        
    @commands.command(aliases = ["courses"])
    async def get_courses(self, ctx):
        courses = self.canvas.get_courses(enrollment_state="active")
        embed = discord.Embed(
            title = 'Available courses',
            description = "Here are all of the courses this bot has access to along with their corresponding codes"
        )
        for course in courses:
            embed.add_field(name = course.name, value = course.id, inline= False)
        await ctx.send(embed=embed)
        
    
    async def send_announcements(self, announcement):
        course_id = int(announcement.context_code[announcement.context_code.index("_")+1:])
        course = self.canvas.get_course(course_id)
        post_datetime = pytz.utc.localize(datetime.datetime.strptime(announcement.posted_at, CANVAS_DATE_FORMAT)).astimezone(IST).strftime(OUTPUT_DATE_FORMAT)

        embed = discord.Embed(
            title = announcement.title,
            description = html2text(announcement.message),
        )
        embed.set_author(name= announcement.author['display_name'], url= announcement.url, icon_url= announcement.author['avatar_image_url'])
        embed.set_footer(text=f'{post_datetime}\n{course.name}')


        for index, channel_id in self.announcement_df[self.announcement_df["Course_ID"]==course_id]["Channel_ID"].iteritems():
            print(f'Sending to {channel_id}')
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed=embed)


    @commands.command(aliases = ['announcements'])
    async def list_announcements(self, ctx):
        embed = discord.Embed(
            title = "Subscribed Canvas courses for this channel",
            description = "This channel is not currently subscribed to any courses for announcements"
        )
        channel_announcements = self.announcement_df[self.announcement_df["Channel_ID"] == ctx.channel.id]
        for index, course_id in channel_announcements.Course_ID.items():
            embed.add_field(name=self.canvas.get_course(course_id), value=" \u200b", inline=False)
            embed.description= "Here are the course announcement subscriptions for this channel"
        await ctx.send(embed=embed)
        
    @commands.command()
    async def add_announcement(self, ctx, course_id):
        course = self.canvas.get_course(course_id)
        self.announcement_df = self.announcement_df.append(pd.DataFrame([[ctx.channel.id, course_id]], columns= self.announcement_df.columns), ignore_index=True)
        embed = discord.Embed(
            title =  'Successfully subscribed to course announcements',
            description = f'This channel will now automatically recieve announcements from Canvas for the specified course. To unsubscribe, use the remove_announcement command'
        )
        embed.add_field(name = 'Course ID', value = course_id)
        embed.add_field(name = 'Course name', value = course.name)
        await ctx.send(embed=embed)
        self.announcement_df.to_csv('csv/Announcements.csv', index = False)
        
        
    @commands.command()
    async def remove_announcement(self, ctx, course_id):
        channel_announcements = self.announcement_df[self.announcement_df["Channel_ID"] == ctx.channel.id]
        to_be_deleted = channel_announcements[channel_announcements["Course_ID"] == course_id]
        self.announcement_df = self.announcement_df.drop(to_be_deleted.index.tolist())
        embed = discord.Embed(
            title =  'Successfully removed Canvas announcement subscription',
            description = f'This channel will no longer automatically recieve announcements from Canvas for:\n{self.canvas.get_course(course_id)}'
        )
        await ctx.send(embed=embed)
        self.announcement_df.to_csv('csv/Announcements.csv', index = False)
        
        
    @tasks.loop(minutes = 1)
    async def clock(self):
        current_datetime = datetime.datetime.now().astimezone(IST)
        time = current_datetime.strftime("%H:%M")
        print(f"Checking for reminders to send at {time}")
        
        reminders_to_send = self.reminder_df[self.reminder_df["Time"] == time].itertuples()
        for reminder in reminders_to_send:
            await self.send_reminder(reminder.Channel_ID, reminder.Course_ID, current_datetime)
        
        print(f"Listening for announcements at {time}")
        courses = self.announcement_df.Course_ID.unique().tolist()
        if courses:
            announcements = self.canvas.get_announcements(context_codes = courses, start_date= self.last_check_time , end_date = current_datetime)
            for announcement in announcements:
                print(f'Sending {announcement}')
                await self.send_announcements(announcement)
    
        self.last_check_time = current_datetime
    

    @clock.before_loop 
    async def before_clock(self):
        await self.bot.wait_until_ready() #Wait for bot to fully start up before starting the automatic due date reminders

def setup(bot):
    bot.add_cog(CanvasCog(bot))
    print("Canvas Cog successfully loaded")
