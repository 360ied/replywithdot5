"""
Tells pokemon names
"""
import logging
from collections import Counter
from string import punctuation

import discord
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from utility.blib import search_google_images, counter_confidence_with_word_list


def get_pokemon_names() -> set:
    # scrapes bulbapedia for a list of pokemon names
    link = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_name"
    get = requests.get(link)
    soup = BeautifulSoup(get.content, features="lxml")

    return {
        unidecode(x.getText()).casefold()  # removes non ascii characters, also casefolds for case insensitive matching
        for x in soup.find_all("a")
        if x.has_attr("href") and x.has_attr("title") and "(Pokémon)" in x["title"]
    }


pokemon_names = get_pokemon_names()

logging.info(f"{len(pokemon_names)} pokemon names found.")


async def run(client: discord.Client, message: discord.Message):
    if len(message.embeds) == 0:
        return
    title = message.embeds[0].title
    if "wild" in title and ("pokémon" in title or "pokemon" in title):
        return
    if message.embeds[0].image == discord.Embed.Empty:
        return

    logging.info(f"Detected spawn in {str(message.channel)}")

    search_result = await search_google_images(message.embeds[0].image.url)

    search_result_text = (''.join(s.findAll(text=True))
                          for s in BeautifulSoup(search_result, features="lxml").findAll('div'))

    counter = Counter((x.rstrip(punctuation).casefold() for y in search_result_text for x in y.split()))

    to_send_list = []

    for element, count, percentage in counter_confidence_with_word_list(counter, pokemon_names):
        to_send_list.append(f"{element}, {percentage}% confidence\n")

    logging.info(f"Most likely spawn: {to_send_list[0]}")

    # bypass Discord 2000 character limit (just in case)
    to_send = ""
    for i in to_send_list:
        if len(to_send + i) > 2000:
            await message.channel.send(to_send)
            to_send = i
        else:
            to_send += i
    await message.channel.send(to_send)
