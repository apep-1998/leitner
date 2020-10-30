from gtts import gTTS
from leitner.settings import MEDIA_ROOT,MEDIA_URL
from os import path

# start web scraping import
from bs4 import BeautifulSoup
import requests
import json
import time
import random
import re
# end web scraping import





def get_voice_name(word):
    return  MEDIA_URL +  word+".mp3"


def get_word_means(word):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    session = requests.session()
    session.get("https://dictionary.cambridge.org/", headers=headers)
    for _ in range(3):
        try:
            resp = session.get("https://dictionary.cambridge.org/dictionary/english/{}".format(word), headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            break
        except Exception as e:
            time.sleep(1)

    head = soup.find_all("div", {"class": "def"})
    means = []
    for h in head:
        mean = h.find_all(text=True, recursive=True)
        mean = mean[:-1]
        mean = "".join(mean).strip().lower()
        mean = mean.replace(";", ".")
        mean = mean.replace(",", ".")
        mean = mean.replace("\n", " ")
        means.append(mean)
    
    #voice
    sources = soup.find_all("source", {"type": "audio/mpeg"})
    voice_file = path.join(MEDIA_ROOT, word+".mp3")
    for source in sources:
        if "us_pron" in source["src"]:
            for _ in range(3):
                try:
                    resp = session.get("https://dictionary.cambridge.org"+source["src"], headers=headers)
                    with open(voice_file, "wb") as vfile:
                        vfile.write(resp.content)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
            break
                        
    return means, voice_file

