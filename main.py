import json
from datetime import date
from pathlib import Path
from random import choice

def get_word_meaning_of_the_day():
    with Path("data", "words.json").open(encoding = "utf-8") as f:
        words: dict = json.load(f)

    w = choice(list(words.keys()))
    return w, choice(words[w])

with open("index.template.html", "r", encoding = "utf-8") as t:
    template = t.read()

calendar_date = date.today().strftime("%A, %B %d, %Y")
daily_word, daily_meaning = get_word_meaning_of_the_day()

index_html = template.format(
    calendar_date = calendar_date,
    daily_word = daily_word,
    daily_meaning = daily_meaning
)

with open("index.html", "w", encoding = "utf-8") as f:
    f.write(index_html)