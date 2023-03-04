from conf import TOKEN, BIBLE_TOKEN, GUILD_ID
import discord
from discord import app_commands
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
        await tree.sync(guild=discord.Object(id=GUILD_ID))

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True



client = Didomi(intents=intents)
tree = app_commands.CommandTree(client)



@tree.command(name="test", description="test",guild = discord.Object(id=GUILD_ID))
async def self(i: discord.Interaction, name:str):
    await i.response.send_message("Same!")

@tree.command(name="fetch", description="test",guild = discord.Object(id=GUILD_ID))
@app_commands.choices(books=[
        app_commands.Choice(name="Genesis", value="GEN"),
        app_commands.Choice(name="Exodus", value="EXO"),
        app_commands.Choice(name="Leviticus", value="LEV"),
        app_commands.Choice(name="Numbers", value="NUM"),
        app_commands.Choice(name="Deuteronomy", value="DEU"),
        app_commands.Choice(name="Joshua", value="JOS"),
        app_commands.Choice(name="Judges", value="JDG"),
        app_commands.Choice(name="Ruth", value="RUT"),
        app_commands.Choice(name="1 Samuel", value="1SA"),
        app_commands.Choice(name="2 Samuel", value="2SA"),
        app_commands.Choice(name="1 Kings", value="1KI"),
        app_commands.Choice(name="2 Kings", value="2KI"),
        app_commands.Choice(name="1 Chronicles", value="1CH"),
        app_commands.Choice(name="2 Chronicles", value="2CH"),
        app_commands.Choice(name="Ezra", value="EZR"),
        app_commands.Choice(name="Nehemiah", value="NEH"),
        app_commands.Choice(name="Esther", value="EST"),
        app_commands.Choice(name="Job", value="JOB"),
        app_commands.Choice(name="Psalms", value="PSA"),
        app_commands.Choice(name="Proverbs", value="PRO"),
        app_commands.Choice(name="Ecclesiastes", value="ECC"),
        app_commands.Choice(name="Song of Solomon", value="SNG"),
        app_commands.Choice(name="Isaiah", value="ISA"),
        app_commands.Choice(name="Jeremiah", value="JER"),
        app_commands.Choice(name="Lamentations", value="LAM"),
        app_commands.Choice(name="Ezekiel", value="EZK"),
        app_commands.Choice(name="Daniel", value="DAN"),
        app_commands.Choice(name="Hosea", value="HOS"),
        app_commands.Choice(name="Joel", value="JOL"),
        app_commands.Choice(name="Amos", value="AMO"),
        app_commands.Choice(name="Obadiah", value="OBA"),
        app_commands.Choice(name="Jonah", value="JON"),
        app_commands.Choice(name="Micah", value="MIC"),
        app_commands.Choice(name="Nahum", value="NAM"),
        app_commands.Choice(name="Habakkuk", value="HAB"),
        app_commands.Choice(name="Zephaniah", value="ZEP"),
        app_commands.Choice(name="Haggai", value="HAG"),
        app_commands.Choice(name="Zechariah", value="ZEC"),
        app_commands.Choice(name="Malachi", value="MAL"),
        app_commands.Choice(name="Matthew", value="MAT"),
        app_commands.Choice(name="Mark", value="MRK"),
        app_commands.Choice(name="Luke", value="LUK"),
        app_commands.Choice(name="John", value="JHN"),
        app_commands.Choice(name="Acts", value="ACT"),
        app_commands.Choice(name="Romans", value="ROM"),
        app_commands.Choice(name="1 Corinthians", value="1CO"),
        app_commands.Choice(name="2 Corinthians", value="2CO"),
        app_commands.Choice(name="Galatians", value="GAL"),
        app_commands.Choice(name="Ephesians", value="EPH"),
        app_commands.Choice(name="Philippians", value="PHP"),
        app_commands.Choice(name="Colossians", value="COL"),
        app_commands.Choice(name="1 Thessalonians", value="1TH"),
        app_commands.Choice(name="2 Thessalonians", value="2TH"),
        app_commands.Choice(name="1 Timothy", value="1TI"),
        app_commands.Choice(name="2 Timothy", value="2TI"),
        app_commands.Choice(name="Titus", value="TIT"),
        app_commands.Choice(name="Philemon", value="PHM"),
        app_commands.Choice(name="Hebrews", value="HEB"),
        app_commands.Choice(name="James", value="JAS"),
        app_commands.Choice(name="1 Peter", value="1PE"),
        app_commands.Choice(name="2 Peter", value="2PE"),
        app_commands.Choice(name="1 John", value="1JN"),
        app_commands.Choice(name="2 John", value="2JN"),
        app_commands.Choice(name="3 John", value="3JN"),
        app_commands.Choice(name="Jude", value="JUD"),
        app_commands.Choice(name="Revelation", value="REV"),
        ])
async def fetch(i: discord.Interaction, books: app_commands.Choice[str], chapter: int, verse:int):
    print(books.value,chapter,verse)
    await i.response.send_message(getVerse(books.value,chapter,verse))

client.run(TOKEN)
