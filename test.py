from conf import BIBLE_TOKEN
import requests
from bs4 import BeautifulSoup

x = requests.get('https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/books',
                 headers={
                     "accept": "application/json",
                     "api-key": BIBLE_TOKEN
                 }
                 )
print(x.json())
"""cnt = x.json()["data"]["content"]

soup = BeautifulSoup(cnt, "html.parser")
print(soup.find("p").text)"""