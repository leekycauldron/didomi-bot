from conf import BIBLE_TOKEN
import requests
from bs4 import BeautifulSoup
import random


x = requests.get('https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/books',
                 headers={
                     "accept": "application/json",
                     "api-key": BIBLE_TOKEN
                 }
                 )
#print(x.json()["data"])
print()
r = random.choice([(0,37),(51,81)])
book = x.json()["data"][random.randint(*r)]["id"]

x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/books/{book}/chapters',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )
l = x.json()["data"]

r = random.randint(1,len(l)-1)



x = requests.get(f'https://api.scripture.api.bible/v1/bibles/9879dbb7cfe39e4d-01/chapters/{book}.{r}/verses',
                    headers={
                        "accept": "application/json",
                        "api-key": BIBLE_TOKEN
                    }
                    )


l = x.json()["data"]
verse = random.randint(0,len(l))
print(book,r,verse)

"""cnt = x.json()["data"]["content"]

soup = BeautifulSoup(cnt, "html.parser")
print(soup.find("p").text)"""