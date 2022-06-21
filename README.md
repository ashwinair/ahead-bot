# ahead-bot
Amrita Ahead Canvas-Telegram-Bot

A Canvas-integration Bot application for the Telegram messaging app.

This bot is self-hosted and runs off of your own individual Canvas API key to access your Canvas courses. Anybody in a server with the bot can use its commands, but it can only access the courses that the canvas account associated with the API key has access to.


Available Commands

By default, all commands will be prefixed with the / symbol in telegram.
    General Commands
        help -> provides information on available commands and usage
        courses -> provides course codes for all available courses that the bot can access
        due -> lists upcoming due dates assignments for a given course id
    Announcement Commands
        sub -> to subscribes a Telegram user chat or a particular group channel for announcements from a given Canvas course 
        unsub -> removes user subscription to a given Canvas course id

Announcements

Announcements are a crucial way for teachers to communicate with students using Canvas LMS. This bot provides a way for users to see announcements in Telegram itself whenever they are posted, because most the communication happens there.

Inner workings

This bot runs a job every 5 minutes to check for new announcements on the Canvas API. If it finds any, it will push this to the people that have subscribed.

If someone subscribes, it'll write this to a subscribers.csv file. This file persists between starts, so subscribers will keep being subscribed if the bot gets restarted.

The bot will both print errors both to the terminal and to a TeleBot.log file.