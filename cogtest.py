import typing
from conf import TOKEN, BIBLE_TOKEN, GUILD_ID
import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import random

from discord.ext import tasks
import discord

@tasks.loop(seconds=1)
async def slow_count():
    print(slow_count.current_loop)


class MyClient(discord.Client):
    async def on_ready(self):
        slow_count.start()


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)