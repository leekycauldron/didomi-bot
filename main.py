from conf import TOKEN, BIBLE_TOKEN
import discord
import requests
from bs4 import BeautifulSoup



def getVerse(book,chapter,verse):
    x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/verses/{book}.{chapter}.{verse}',
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

        if message.content.startswith("fetch"):
            stuff = message.content[6:].split(":")
            
            book = stuff[0]
            chapter = stuff[1]
            verse = stuff[2]
           
            await message.channel.send(getVerse(book,chapter,verse)) 
intents = discord.Intents.default()
intents.message_content = True

client = Didomi(intents=intents)
client.run(TOKEN)
