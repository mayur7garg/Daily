import json
from datetime import date
from pathlib import Path
from random import choice, randint

def get_deck_date(d: date):
    doy = d.timetuple().tm_yday - 1

    if doy == 364:
        deck_date = "Day of the Joker"
    elif doy == 365:
        deck_date = "Day of the Deck"
    else:
        planet = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"][doy % 7]
        suit = ["Spades", "Hearts", "Diamonds", "Clubs"][(doy // 7) % 4]
        card = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"][(doy // 28) % 13]
    
        deck_date = f"{card} of {suit}, Day of {planet}"

    return deck_date

def get_word_meaning_of_the_day():
    with Path("data", "words.json").open(encoding = "utf-8") as f:
        words: dict = json.load(f)

    w = choice(list(words.keys()))
    return w, choice(words[w])

def get_shlok():
    with Path("data", "Bhagwad_Gita.json").open(encoding = "utf-8") as f:
        shloks: dict = json.load(f)

    shlok_id = choice(list(shloks.keys()))
    return shloks[shlok_id]

with open("index.template.html", "r", encoding = "utf-8") as t:
    template = t.read()

bg_color = f'style="background-color: rgb({randint(0, 150)}, {randint(0, 150)}, {randint(0, 150)});"'
calendar_date = date.today().strftime("%A, %B %d, %Y")
deck_date = get_deck_date(date.today())
daily_word, daily_meaning = get_word_meaning_of_the_day()
shlok = get_shlok()

index_html = template.format(
    bg_color = bg_color,
    calendar_date = calendar_date,
    deck_date = deck_date,
    daily_word = daily_word,
    daily_meaning = daily_meaning,
    daily_shlok_chapter = shlok['Chapter'],
    daily_shlok_verse = shlok['Verse'],
    daily_shlok = shlok['Shloka'],
    daily_shlok_meaning = shlok['EngMeaning']
)

with open("index.html", "w", encoding = "utf-8") as f:
    f.write(index_html)