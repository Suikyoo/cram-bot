import os, discord, random
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook

intents = discord.Intents.default()
intents.message_content = True
token = "MTE3MDM0ODI3MDc4MzA0MTU4OA.GQxl2K.EERx7fNGKlpyBUD0ZOp-xrNCZkyYy03c5XbQCM"
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def test(ctx, text):
    print(bot.get_channel(1170351793776115774))
    await bot.get_channel(1170351793776115774).send(text)


bot.run(token)
