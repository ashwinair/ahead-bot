# AheadLMS-bot 

**Amrita Ahead Canvas LMS Telegram Bot** 


A Canvas-integration Bot application for the Telegram messaging app.

This bot is self-hosted and runs off of your own individual Canvas API key to access your Canvas courses. Anybody in a server with the bot can use its commands, but it can only access the courses that the canvas account associated with the API key has access to.


## Available Commands
By default, all commands will be prefixed with the `/` symbol in telegram.
 - **General Commands**
    - `help` - provides information on available commands and usage
    - `courses` - provides course codes for all available courses that the bot can access
    - `due` - lists upcoming due dates assignments for a given course id
    
    ![General Commands](https://user-images.githubusercontent.com/58840757/180377635-113e1dd7-3fcf-4e87-a7b7-b899f589349e.jpg)
    ![due](https://user-images.githubusercontent.com/58840757/180377829-d03fb40b-6578-4e07-9f96-bf40ed2e88f6.jpg)


### Announcements
Announcements are a crucial way for teachers to communicate with students using Canvas LMS. This bot provides a way for users to see announcements in Telegram itself whenever they are posted, because most the communication happens there.

 -  **Announcement Commands**
    -  `sub` - to subscribes a Telegram user chat or a particular group channel for announcements from a given Canvas course
    -  `unsub` - removes user subscription to a given Canvas course id
     
![Announcement Commands](https://user-images.githubusercontent.com/58840757/180376672-fa97b739-b8b0-463b-899c-14277d3d1e86.png)


## Inner workings

This bot runs a job every 5 minutes to check for new announcements on the Canvas API. If it finds any, it will push this to the people that have subscribed.

If someone subscribes, it'll write this to a subscribers.csv file. This file persists between starts, so subscribers will keep being subscribed if the bot gets restarted.

The bot will both print errors both to the terminal and to a TeleBot.log file.

## Dependencies

The bot requires the following pip packages:

- `python-telegram-bot==20.0a0`
- `aiohttp`
- `canvasapi`
- `datetime`
- `html2text`
- `pandas`
- `pytz`
- `requests`


You can install all of them using `pip install -r requirements.txt`.

## Create your own instance of the Bot
Since the bot can only run on an individual API Key, users can only set up a working bot for their own Canvas courses.
You can create your own Telegram Bot and run it with the code in this repository, using your own API keys instead. To do this you will need to:
### 1. Clone this repository
Type `git clone https://github.com/ashwinair/ahead-bot.git` in your command line or download from the main page of the repo. Initially you need to clear the subscribers.csv files except for the first line so that you can have your own reminders rather than that of this template bot.
### 2. Generate a Canvas API token
Here is a [step-by-step tutorial to generate your Canvas API token](https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273)
### 3. Create a Telegram Bot
Refer to [Telegram Documentation for this](https://core.telegram.org/bots#3-how-do-i-create-a-bot), and get your Telegram bot API Key.
### 4. Change the following lines in [/tele/constants.py](https://github.com/ashwinair/ahead-bot/blob/main/tele/constants.py) with your details
```python
API_KEY = 'Your Telegram API KEY'
CANVAS_URL = 'Your CANVAS DOMAIN'
CANVAS_TOKEN = 'Your CANVAS TOKEN ID'
```
### 5. Run it on Repl.it
### 6. Create account on [UptimeRobot](https://uptimerobot.com) to ping the bot at any particular interval to keep it alive :)
[![Run on Repl.it](https://repl.it/badge/github/ashwinair/ahead-bot)](https://repl.it/github/ashwinair/ahead-bot)
