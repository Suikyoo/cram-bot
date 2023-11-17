from discord.ext import tasks
from bot_data import bot_data, bot, channel_id, token
from commands import commands, command_prefix

async def ask_question():
    await bot.wait_until_ready()
    bot_data.load_question() 
    if bot_data.current_item:
        await bot.get_channel(channel_id).send("```" + bot_data.current_item.question + "```")
    else:
        await bot.get_channel(channel_id).send("```Out of questions. Exiting Command...```")
        bot_data.reset()

@bot.event
async def on_ready():
    flash_card.start()
    print(f"Logged in as {bot.user}")
    await bot.get_channel(channel_id).send(f'`Hello! I\'m back.`')

@bot.event
async def on_message(msg):
    await bot.wait_until_ready()

    if msg.channel == bot.get_channel(channel_id):
        if bot_data.state == "flash_card":
            if msg.author != bot.user:
                bot_data.queue_msg(msg)

        #command register mechanic
        if len(msg.content):
            if msg.content[0] == command_prefix:
                cmd_info = msg.content[1:].lower().split(" ")
                if cmd_info[0] in commands:
                    try:
                        await commands[cmd_info[0]](msg, *cmd_info[1:])

                    except TypeError:
                        await bot.get_channel(channel_id).send("`wrong or missing arguments for the command`")

                else:
                    await bot.get_channel(channel_id).send("`command not recognized`")

@tasks.loop(seconds=2.0)
async def flash_card():
    if bot_data.state == "flash_card":
        if not bot_data.current_item:
            await ask_question()
        else:
            for msg in bot_data.msg_queue:
                answer_status = bot_data.check_answer(msg.content)
                if answer_status == 1:
                    await msg.reply(f'{msg.author} got the correct answer!')
                    await msg.channel.send(f'`          -----Next Question-----          `')
                    bot_data.close_question()
                    break

                if answer_status == 2:
                    fraction = bot_data.current_item.get_answer_fraction()
                    await msg.reply(f'{msg.author} got one of the answers! answer({fraction[0]}/{fraction[1]})')

                    if fraction[0] == fraction[1]:
                        await msg.reply(f'Question is fully answered')
                        await msg.channel.send(f'`          -----Next Question-----          `')
                        bot_data.close_question()
                        break
                        
            bot_data.clear_msg_queue()

bot.run(token)
