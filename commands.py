import discord
from bot_data import bot_data, bot

commands = {}
command_prefix = "!"

intents = discord.Intents.default()

def reg_command(funct, *custom_name):
    if len(custom_name):
        commands[custom_name[0]] = funct
    else: 
        commands[funct.__name__] = funct

@reg_command
async def test(msg, text):
    await msg.channel.send("`" + text + "`")

@reg_command
async def start(msg, db_name):
    load_status = bot_data.load_db(db_name)
    
    if not load_status:
        await msg.channel.send(f'`No such database in the system`')
    else:
        bot_data.set_state("flash_card")
        await msg.channel.send(f'`          -----Start Quiz-----          `')

@reg_command
async def skip_question(msg):
    if bot_data.state == "flash_card":
        bot_data.skip_question()
        await msg.channel.send("`Question Skipped`")

@reg_command
async def pass_question(msg):
    if bot_data.state == "flash_card":
        bot_data.pass_question()
        await msg.channel.send("`Question Passed`")

@reg_command
async def reveal_answer(msg):
    if bot_data.state == "flash_card":
        await msg.channel.send(f'```{bot_data.get_answers_repr()}```')

@reg_command
async def list_db(msg):
    await msg.channel.send(f'```{bot_data.get_db_list_repr()}```')

@reg_command
async def db(msg):
    await msg.channel.send(f'`{bot_data.get_current_db_repr()}`')

@reg_command
async def stop(msg):
    await msg.channel.send("`Quiz Stopped`")

    bot_data.reset()

@reg_command
async def help_command(msg):
    await msg.channel.send(f'```Commands: \n{bot_data.enumerate_repr(list(commands.keys()))}```')

commands["pass"] = commands.pop("pass_question")
commands["skip"] = commands.pop("skip_question")
commands["reveal"] = commands.pop("reveal_answer")
commands["list"] = commands.pop("list_db")
commands["help"] = commands.pop("help_command")
