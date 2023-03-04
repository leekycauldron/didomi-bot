from conf import TOKEN, BIBLE_TOKEN
import discord
import requests
from bs4 import BeautifulSoup


def getVerse(chapter,verse):
    x = requests.get('https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/verses/GEN.1.1',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )
    cnt = x.json()["data"]["content"]

    soup = BeautifulSoup(cnt, "html.parser")
    return soup.find("p").text


##########################################
class Didomi(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
    
        print(f'Message from {message.author}: {message.content}')

        if "verse" in message.content:
            await message.channel.send(getVerse(1,1)) 

intents = discord.Intents.default()
intents.message_content = True

client = Didomi(intents=intents)
client.run(TOKEN)
