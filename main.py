from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import canvas
from telegram import ForceReply, Update
import jsonpickle
import json
from rapidfuzz.distance import Indel
# from canvasapi import Canvas
API_KEY = '5460223513:AAFLCOuUnTAcX175NtPphOxss0Ghi7acYqo'
# bot = telebot.TeleBot(API_KEY)
CANVAS_URL = 'https://aheadonline.amrita.edu'
CANVAS_TOKEN = 'yxDlbHuvnLUvX28wlbhtK9pu018QCz6pE2o0rrpXfWZG8tI2iyUfzp1B4SztRGr7'
# retriver = canvas.Canvas(CANVAS_URL, CANVAS_TOKEN )

# canvas_proxy = Canvas(CANVAS_URL, CANVAS_TOKEN)

# def convert_to_json(message):
#     json_str = jsonpickle.encode(message)
#     return json.loads(json_str)

canvas_client = canvas.CanvasTele(CANVAS_URL,CANVAS_TOKEN)

async def start(update,context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup = ForceReply(selective=True),
    ) 

def whatis(update,context):
    msg = update.message
    # print(update.message)
    querie = msg['text']
    querie = querie[5:]
    print(querie)
    print(Indel.normalized_similarity(querie.strip(), 'next semesters?'))

def main():
    application = Application.builder().token(API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("what", whatis))
    application.add_handler(CommandHandler("courses", canvas_client.get_courses_list))
    application.add_handler(CommandHandler("ass", canvas_client.get_all_assingmets))


    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
