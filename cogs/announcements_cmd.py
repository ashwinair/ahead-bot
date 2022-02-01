import discord
from discord.ext import commands


class announcements_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title="Help", description="Use !help <command> for more information about that command.",
                           colour=ctx.author.color)
        em.add_field(name="Get Course", value="get_course")
        em.add_field(name="Announcement commands", value="add_announcement, remove_announcement, list_announcements")

        em.add_field(name="Have Suggestions?",
                     value="for now there is only one command if you have any suggestion ping @ashwin in suggestions "
                           "channel. :)")

        await ctx.send(embed=em)

    @help.command()
    async def get_courses(self, ctx):
        em = discord.Embed(title="Get Course",
                           description="Displays all courses along with corresponding codes that the bot has access to",
                           color=ctx.author.color)
        em.add_field(name="How to use:", value="!get_course <course_code>")
        em.add_field(name="Aliases:", value="!courses")
        await ctx.send(embed=em)

    @help.command()
    async def add_announcement(self, ctx):
        em = discord.Embed(title="Add Announcement",
                           description="Subscribes a channel to a Canvas course for announcements",
                           color=ctx.author.color)
        em.add_field(name="How to use:", value="!add_announcement <course_code>")
        em.add_field(name="Variables:",
                     value="*course_code*: Use !get_courses to get the course code of the announcement you want to add",
                     inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def remove_announcement(self, ctx):
        em = discord.Embed(title="Remove Announcements", description="Removes an announcement", color=ctx.author.color)
        em.add_field(name="How to use:", value="!remove_announcement <course_code>")
        em.add_field(name="Variables:",
                     value="*course_code*: use !get_courses to get the course code of the announcement you want to "
                           "remove",
                     inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def list_announcements(self, ctx):
        em = discord.Embed(title="List Announcements",
                           description="Displays current Canvas course announcement subscriptions in this channel",
                           color=ctx.author.color)
        em.add_field(name="How to use:", value=">list_announcements")
        em.add_field(name="Aliases:", value=">announcements", inline=False)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(announcements_cmd(bot))
    print("announcements_cmd Cog successfully loaded")
