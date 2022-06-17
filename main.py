from datetime import datetime
from queue import Queue
from telegram.ext import (
    Application,
    CommandHandler,
    Updater, 
    JobQueue
)
import canvas_handler
from telegram import ForceReply, Update,Bot
from tele.constants import(
    CANVAS_URL,
    CANVAS_TOKEN,
    API_KEY
)
# retriver = canvas.Canvas(CANVAS_URL, CANVAS_TOKEN )

# canvas_proxy = Canvas(CANVAS_URL, CANVAS_TOKEN)

# def convert_to_json(message):
#     json_str = jsonpickle.encode(message)
#     return json.loads(json_str)

canvas_client = canvas_handler.CanvasTele(CANVAS_URL,CANVAS_TOKEN)

async def start(update,context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup = ForceReply(selective=True),
    )
    
async def help(update,context) -> None:
    """List the commands available to the user"""
    text_to_send = """I will send you remainders for your assignments of every subject before the due date\n\t
    To get the list of courses use command /courses \n
    To ask any gernal querie use command /ask <your querie>,\n 
    i will try to answer :)\n"""
    await update.message.reply_text(text_to_send)

def main():
    # application = Application.builder().token(API_KEY).build()
    application = Application.builder().token(API_KEY).build()

    job_queue = application.job_queue
    # job_queue.run_repeating(callback=canvas_client.get_annoucements,
    #         interval=60)
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("courses", canvas_client.get_courses_list))
    application.add_handler(CommandHandler("due", canvas_client.get_assingment))

    #job.run_repeating(,interval= 10,first=0)
    # application.add_error_handler(error)
    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    #updater.idle()
if __name__ == "__main__":
    main()
