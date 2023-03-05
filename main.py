import typing
from conf import TOKEN, BIBLE_TOKEN, GUILD_ID, AI_KEY
from text import SETUP, personalities
import discord
from discord import app_commands
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup
import random
import datetime
import openai
import os
import asyncio

openai.api_key = AI_KEY
DEMO = False

chats = []
books = {"Genesis":"GEN",
        "Exodus":"EXO",
        "Leviticus":"LEV",
        "Numbers":"NUM",
        "Deuteronomy":"DEU",
        "Joshua":"JOS",
        "Judges":"JDG",
        "Ruth":"RUT",
        "1 Samuel":"1SA",
        "2 Samuel":"2SA",
        "1 Kings":"1KI",
        "2 Kings":"2KI",
        "1 Chronicles":"1CH",
        "2 Chronicles":"2CH",
        "Ezra":"EZR",
        "Nehemiah":"NEH",
        "Esther":"EST",
        "Job":"JOB",
        "Psalms":"PSA",
        "Proverbs":"PRO",
        "Ecclesiastes":"ECC",
        "Song of Solomon":"SNG",
        "Isaiah":"ISA",
        "Jeremiah":"JER",
        "Lamentations":"LAM",
        "Ezekiel":"EZK",
        "Daniel":"DAN",
        "Hosea":"HOS",
        "Joel":"JOL",
        "Amos":"AMO",
        "Obadiah":"OBA",
        "Jonah":"JON",
        "Micah":"MIC",
        "Nahum":"NAM",
        "Habakkuk":"HAB",
        "Zephaniah":"ZEP",
        "Haggai":"HAG",
        "Zechariah":"ZEC",
        "Malachi":"MAL",
        "Matthew":"MAT",
        "Mark":"MRK",
        "Luke":"LUK",
        "John":"JHN",
        "Acts":"ACT",
        "Romans":"ROM",
        "1 Corinthians":"1CO",
        "2 Corinthians":"2CO",
        "Galatians":"GAL",
        "Ephesians":"EPH",
        "Philippians":"PHP",
        "Colossians":"COL",
        "1 Thessalonians":"1TH",
        "2 Thessalonians":"2TH",
        "1 Timothy":"1TI",
        "2 Timothy":"2TI",
        "Titus":"TIT",
        "Philemon":"PHM",
        "Hebrews":"HEB",
        "James":"JAS",
        "1 Peter":"1PE",
        "2 Peter":"2PE",
        "1 John":"1JN",
        "2 John":"2JN",
        "3 John":"3JN",
        "Jude":"JUD",
        "Revelation":"REV",}

# Gets a specified Verse
def getVerse(book,chapter,verse):
    x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/verses/{book}.{chapter}.{verse}',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )
    cnt = x.json()["data"]["content"]

    soup = BeautifulSoup(cnt, "html.parser")
    v = soup.find("p").text

    idx = 0
    # get idx of first letter
    for i in range(len(v)):
        if not (str(v[i]).isdigit()):
            idx = i
            break
    print(idx)
    ref = x.json()["data"]["reference"]
    return ref + " `" + v[idx:] + "`"


#Gets a random verse in a random chapter in a random book.
def getRand():
    # Get a random book
    
    x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/books',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )
    r = random.choice([(0,37),(52,80)])
    book = x.json()["data"][random.randint(*r)]["id"]
    x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/books/{book}/chapters',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )
    l = x.json()["data"]
    chapter = random.randint(1,len(l)-1)
    x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/chapters/{book}.{chapter}/verses',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )


    l = x.json()["data"]
    verse = random.randint(0,len(l))
    return getVerse(book,chapter,verse)

def getDaily():
    f = open("daily.txt", "r")
    x= f.readline()
    f.close()
    return x
    
def setDaily():
    with open("daily.txt","w") as f:
        f.write(getRand())
    
##########################################

#Get and Store daily verse
@tasks.loop(seconds=60)
async def daily_verse():
    if DEMO or (datetime.datetime.now().strftime("%H") == 00 and datetime.datetime.now().strftime("%M") == 00):
        # Set new verse at 12AM or if demo version (every 30 seconds)
        print("Setting daily verse..")
        while True:
            try:
                setDaily()
                break
            except:
                continue


class Didomi(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await tree.sync(guild=discord.Object(id=GUILD_ID))
        daily_verse.start()
        

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        uid = message.author.id
        channel_id = message.channel.id
        for chat in range(len(chats)):
            # Check if user and channel match an existing chat.
            messages = chats[chat][3]
            if uid == chats[chat][2] and channel_id == chats[chat][1]:
                if message:
                    messages.append(
                        {"role": "user", "content": message.content}
                    )
                    c = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages
                    )
                    reply = c.choices[0].message.content
                    await message.channel.send(reply,reference=message)
                    print(reply)
                    messages.append({"role":"assistant","content":reply})
                break


intents = discord.Intents.default()
intents.message_content = True



client = Didomi(intents=intents)
tree = app_commands.CommandTree(client)


###################
#FUNCTIONS:
####################
"""@tree.command(name="help", description="Explains all commands in more depth, as well as the purpose of this bot!",guild = discord.Object(id=GUILD_ID))
async def help(i: discord.Interaction):
    helptext = "```"
    for command in tree.get_commands(guild = discord.Object(id=GUILD_ID)):
        helptext+=f"{command.name} - {command.description}\n\n"
    helptext+="```"
    await i.response.send_message(helptext)"""
#######################################################


async def autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    books = ["Genesis",
        "Exodus",
        "Leviticus",
        "Numbers",
        "Deuteronomy",
        "Joshua",
        "Judges",
        "Ruth",
        "1 Samuel",
        "2 Samuel",
        "1 Kings",
        "2 Kings",
        "1 Chronicles",
        "2 Chronicles",
        "Ezra",
        "Nehemiah",
        "Esther",
        "Job",
        "Psalms",
        "Proverbs",
        "Ecclesiastes",
        "Song of Solomon",
        "Isaiah",
        "Jeremiah",
        "Lamentations",
        "Ezekiel",
        "Daniel",
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
        "Matthew",
        "Mark",
        "Luke",
        "John",
        "Acts",
        "Romans",
        "1 Corinthians",
        "2 Corinthians",
        "Galatians",
        "Ephesians",
        "Philippians",
        "Colossians",
        "1 Thessalonians",
        "2 Thessalonians",
        "1 Timothy",
        "2 Timothy",
        "Titus",
        "Philemon",
        "Hebrews",
        "James",
        "1 Peter",
        "2 Peter",
        "1 John",
        "2 John",
        "3 John",
        "Jude",
        "Revelation"]
    return [
        app_commands.Choice(name=book, value=book)
        for book in books if current.lower() in book.lower()
    ]

@tree.command(name="fetch", description="Search for a bible verse of your choosing!",guild = discord.Object(id=GUILD_ID))
@app_commands.autocomplete(book=autocomplete)
async def fetch(i: discord.Interaction, book:str, chapter: int, verse:int):
    await i.response.send_message(getVerse(books[book],chapter,verse))

###############################################################
@tree.command(name="rand", description="Get a random verse from the bible!",guild = discord.Object(id=GUILD_ID))
async def rand(i: discord.Interaction):
    await i.response.send_message(getRand())
###############################################################
@tree.command(name="daily", description="Get the verse of the day!",guild = discord.Object(id=GUILD_ID))
async def rand(i: discord.Interaction):
    await i.response.send_message(getDaily())
###############################################################
async def autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    persons = [
        "Sarah"
    ]
    return [
        app_commands.Choice(name=person, value=person)
        for person in persons if current.lower() in person.lower()
    ]
@app_commands.autocomplete(person=autocomplete)
@tree.command(name="start", description="Start a chat with me!",guild = discord.Object(id=GUILD_ID))
async def start(i: discord.Interaction, person:str=None):
    await i.response.defer(ephemeral=True)
    await asyncio.sleep(3)
    id = 0
    chat_channel = i.channel.id
    uid = i.user.id
    if person:
        messages = [
        {"role":"system","content":personalities[person]}
    ]
    else:
        messages = [
            {"role":"system","content":SETUP}
        ]

    is_in = False
    for chat in range(len(chats)):
        if i.user.id == chats[chat][2]:
            is_in = True
            await i.followup.send("❌ You already have a chat running! Run `/end` to stop.")
            break
    if not is_in:
        
        if os.path.exists(os.path.join("users",str(i.user.id)+".txt")): # check if user has had a previous conversation
            with open(os.path.join("users",str(i.user.id)+".txt"),"r") as f:
                
                message =  " use this information about me for our conversation: " + f.read()
                ms = messages.copy()
                
                ms.append(
                    {"role": "user", "content": message}
                )
                c = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=ms
                )
                reply = c.choices[0].message.content
                ms.append({"role":"assistant","content":reply})
                chats.append([id,chat_channel,uid,ms.copy()])
        else:
            chats.append([id,chat_channel,uid,messages.copy()])
        
        await i.followup.send("👋 Hi, I'm Didomi! Ask me anything! Run `/end` to stop.")
        print(chats)
###############################################################
@tree.command(name="end", description="Ends the current chat.",guild = discord.Object(id=GUILD_ID))
async def end(i: discord.Interaction):
    await i.response.defer(ephemeral=True)
    await asyncio.sleep(3)
    for chat in range(len(chats)):
        if i.user.id == chats[chat][2]:
            # Save summary to database.
            with open(os.path.join("users",str(i.user.id)+".txt"),"w") as f:
                message = "summarize our conversation and dont forget the summary i gave you at the start and remember things about me"
                messages = chats[chat][3]
                messages.append(
                    {"role": "user", "content": message}
                )
                c = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )
                reply = c.choices[0].message.content
                print("SUMMARY: " + reply)
                f.write(reply)
            chats.pop(chat)
            break
    
    await i.followup.send("Goodbye!")

client.run(TOKEN)
