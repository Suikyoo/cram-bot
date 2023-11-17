import os, discord, random
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook

class Item:
    def __init__(self , answer, question):
        self.answer = answer
        self.question = question
        #AND check
        if isinstance(answer, str):
            self.answer_buffer = answer.split("&")
        
            for i in range(len(self.answer_buffer)):
                #OR check
                self.answer_buffer[i] = [" ".join(j.strip().split()) for j in self.answer_buffer[i].split("|")]
        else: 
            self.answer_buffer = [[answer]]

        self.answer_amt = len(self.answer_buffer)
        self.answer_buffer_origin = self.answer_buffer.copy()

    def check_answer(self, answer):
        for i in range(len(self.answer_buffer)):
            if answer.lower() in [str(j).lower() for j in self.answer_buffer[i]]:
                self.answer_buffer.pop(i)
                return True

    def get_raw_data(self):
        return [self.answer, self.question]

    def get_answer_fraction(self):
        return (self.answer_amt - len(self.answer_buffer), self.answer_amt)

class BotData:
    def __init__(self):
        self.msg_queue = []
        self.state = "idle"

        #db = [[answer, question], ...]
        self.db = None
        self.db_name = ""

        self.presented_questions = []
        self.completed_questions = []
        self.current_item = None

    def reset(self):
        self.msg_queue = []
        self.set_state("idle")
        self.db = None
        #questions are raw tuples containing data for Item-type instances
        self.presented_questions = []
        self.completed_questions = []
        self.current_item = None


    def load_db(self, db_name):
        try:
            wb = load_workbook(f'{db_name}.xlsx')
            ws = wb.active
            rows = ws.values
            self.db = [list(i)[:2] for i in rows]
            self.db_name = db_name
            self.presented_questions = self.db.copy()

            return True

        except FileNotFoundError:
            return False

    def load_question(self):
        if len(self.presented_questions):
            self.current_item = Item(*random.choice(self.presented_questions))

    def skip_question(self):
        self.close_question()

    def pass_question(self):
        self.current_item = None

    def close_question(self):
        self.presented_questions.remove(self.current_item.get_raw_data())
        self.completed_questions.append(self.current_item.get_raw_data())
        self.current_item = None

    #returns 3 possible states
    #0=wrong, 1=correct, 2=partially correct(enumeration type)
    def check_answer(self, answer):
        check = self.current_item.check_answer(answer)
        if check:
            if self.current_item.answer_amt == 1:
                return 1
            
            else:
                return 2

        else:
            return 0

    def enumerate_repr(self, lst):
        num = 0
        string = ""
        if len(lst):
            for i in lst:
                num += 1
                string += f'{num}. {i}\n'
        else:
            string += f'{lst[0]}'

        return string


    def get_answers_repr(self):
        return "Answer:\n" + self.enumerate_repr([i[0] for i in self.current_item.answer_buffer_origin])
        

    def get_current_db_repr(self):
        string = "Answer:\n"
        string += f'{self.db_name}'
        return string

    def get_db_list_repr(self):
        return "Database:\n" + self.enumerate_repr([os.path.splitext(file)[0] for file in os.listdir(".") if os.path.splitext(file)[1] == ".xlsx"])

    def get_state(self, state):
        return self.state

    def set_state(self, state):
        self.state = state

    def queue_msg(self, msg):
        self.msg_queue += [msg]

    def clear_msg_queue(self):
        self.msg_queue = []

bot_data = BotData()

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = discord.Client(intents=intents)
channel_id = 1171635547144466574 


