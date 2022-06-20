from datetime import datetime
from telegram.ext import (
    Application,
    CommandHandler,
)
from tele.pattern_matching import Pattern_Matching
import canvas_handler
from telegram import ForceReply, Update
from tele.constants import(
    CANVAS_URL,
    CANVAS_TOKEN,
    API_KEY
)
from tele.subscribe_manager import SubscribeManager

canvas_client = canvas_handler.CanvasTele(CANVAS_URL, CANVAS_TOKEN)
sub = SubscribeManager(CANVAS_URL, CANVAS_TOKEN)

async def start(update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help(update, context) -> None:
    text_to_send = """
    List of commands available:\t
    
⇝ /courses - To get the list of courses use command 
    
⇝ /due - To get list of assignments for all subjects. 
    
⇝ /sub - To subscribe to a particular course announcements. 
    
⇝ /unsub - To unsubscribe to a particular  course announcements.
    """
    await update.message.reply_text(text_to_send)


def main():
    application = Application.builder().token(API_KEY).build()
    job_queue = application.job_queue
    job_queue.run_repeating(callback=canvas_client.get_annoucements,
                            interval=60)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("courses", canvas_client.get_courses_list))
    application.add_handler(CommandHandler("due", canvas_client.get_assingment))
    application.add_handler(CommandHandler("ask", Pattern_Matching.matching))
    application.add_handler(CommandHandler("sub", sub.subscribe_announcement))
    application.add_handler(CommandHandler("unsub", sub.unsubscribe))
    application.run_polling()


if __name__ == "__main__":
    main()
