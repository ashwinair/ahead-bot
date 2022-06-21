from canvasapi import Canvas
import pandas as pd



class SubscribeManager:
    
    def __init__(self,Canvas_URL, CANVAS_TOKEN):
        self.announcements_df= pd.read_csv('csv/subscribers.csv',dtype='int64',error_bad_lines=False)
        self.canvas = Canvas(Canvas_URL, CANVAS_TOKEN) 
        
    def sub_message_format(self,title,description,course_id):
        '''Format the Subscribe and Unsubscribe announcement message'''
        course = self.canvas.get_course(course_id)
        message = []
        message.append(f'Sucessfully {title} to the {course.name} announcements. :)\n\t')
        message.append(description) 
        return message
            
    async def subscribe_announcement(self,update, context):
        '''Subscribe the user for the specified course id and update subscribers.csv'''
        msg = update.message['text']
        chat_id = update.message['chat_id']
        # remove the command, '/sub', from the string and get the course id give by user
        course_id = msg[4:].strip()
        # print(course_id)
        if course_id == '':
            await update.message.reply_text('Please enter a <course id> with /sub command to subscribe.\n -> /sub <course_id>')
        else:
            try:
                # convert the message/course id to int
                course_id = int(course_id)
                is_valid_course = bool(self.canvas.get_course(course_id))
                is_already_subscribed = False
                if is_valid_course:
                    for index, row in self.announcements_df.iterrows():
                        if (row['Chat_ID'] == chat_id) and (row['Course_id'] == course_id):
                            is_already_subscribed = True
                        
                    if is_already_subscribed :
                        await update.message.reply_text('You have already subscribed to this course announcements. :)')
                    else:
                        self.announcements_df = self.announcements_df.append(pd.DataFrame(
                            [[chat_id, course_id]], columns= self.announcements_df.columns), ignore_index=True)
                        title =  'subscribed'
                        description = 'This channel will now automatically recieve announcements from Canvas for the specified course. To unsubscribe, use the /unsub command'
                        self.announcements_df.to_csv('csv/subscribers.csv', index = False)
                        formated_sub_message = self.sub_message_format(title,description,course_id)
                        text_to_send = '\n'.join(formated_sub_message)
                        await update.message.reply_text(text_to_send)                    
                else:
                    await update.message.reply_text("Please enter a valid course id :/")
            except:  # message is not type int...
                return await update.message.reply_text("Please enter a valid integer value :/ \n type -> /courses to get the list of available courses with there ids ")
            
    async def unsubscribe(self,update,context):
        '''Unsubscribe the user from the particular course id and update subscribers.csv'''
        msg = update.message['text']
        chat_id = update.message['chat_id']
        # remove the command, '/unsub', from the string and get the course id give by user
        course_id = msg[6:].strip()
        # print(course_id)
        if course_id == '':
            await update.message.reply_text('Please enter a <course id> with /unsub command to subscribe.\n -> /unsub <course_id>')
        else:
            try:
                # convert the message/course id to int
                course_id = int(course_id)
                is_valid_course = bool(self.canvas.get_course(course_id))
                is_already_subscribed = False
                value_index = 0
                if is_valid_course:
                    for index, row in self.announcements_df.iterrows():
                        if (row['Chat_ID'] == chat_id) and (row['Course_id'] == course_id):
                            is_already_subscribed = True
                            value_index = index
                    if is_already_subscribed :
                        self.announcements_df = self.announcements_df.drop(value_index)
                        self.announcements_df.to_csv('csv/subscribers.csv', index = False)
                        title =  'unsubscribed'
                        description = 'This channel will no longer automatically recieve announcements from Canvas for the specified course.'
                        self.announcements_df.to_csv('csv/subscribers.csv', index = False)
                        formated_sub_message = self.sub_message_format(title,description,course_id)
                        text_to_send = '\n'.join(formated_sub_message)
                        await update.message.reply_text(text_to_send)
                    else:
                        await update.message.reply_text('You have not subscribed to this course announcements. :)')                   
                else:
                    await update.message.reply_text("Please enter a valid course id :/")
            except:  # message is not type int...
                return await update.message.reply_text("Please enter a valid integer value :/ \n type -> /courses to get the list of available courses with there ids ")