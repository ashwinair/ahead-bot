from datetime import datetime
from canvasapi import Canvas
import pytz
IST = pytz.timezone('Asia/Kolkata')
CANVAS_DATE_FORMAT = r'%Y-%m-%dT%H:%M:%SZ'
OUTPUT_DATE_FORMAT = r'%a, %b %d at %I:%M %p'

class Assignments:
    
    def __init__(self,API_URL, CANVAS_TOKEN):
        self.canvas = Canvas(API_URL, CANVAS_TOKEN)  
        
          
    def get_assignment_formatted(self,course,assignments_list,due_date_list):
        assignments_texts = []
        assignments_texts.append(f'Assignments dues for {course}: \n')
        for x in range(0,len(assignments_list)):
            title = assignments_list[x]
            last_date = due_date_list[x]
            assignments_texts.append('Title:  {}\n\tTime:  {}\n\t'
                                    .format(title, last_date))
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
            print(f"no assignments reminder for {course.name} today.")
            await update.message.reply_text(f"no assignments reminder for {course.name} today.")
            return  # If there aren't any assignments due today, don't send a reminder
        formatted_assignments = self.get_assignment_formatted(course.name,assignments_list ,due_date_list)
        text_to_send = '\n'.join(formatted_assignments)
        await update.message.reply_text(text_to_send)
