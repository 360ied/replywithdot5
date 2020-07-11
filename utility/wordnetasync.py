"""Better version of https://github.com/geekpradd/PyDictionary"""
import re

import aiohttp
from bs4 import BeautifulSoup


async def _get_soup_object(url, parser="html.parser"):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return BeautifulSoup(await response.read(), parser=parser)


async def synonym(term, formatted=False):
    data = await _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
    section = data.find('div', {'class': 'type-synonym'})
    spans = section.findAll('a')
    synonyms = [span.text.strip() for span in spans]
    if formatted:
        return {term: synonyms}
    return synonyms


async def antonym(term, formatted=False):
    data = await _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
    section = data.find('div', {'class': 'type-antonym'})
    spans = section.findAll('a')
    antonyms = [span.text.strip() for span in spans]
    if formatted:
        return {term: antonyms}
    return antonyms


async def meaning(term):
    html = await _get_soup_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
        term))
    types = html.findAll("h3")
    lists = html.findAll("ul")
    out = {}
    for a in types:
        reg = str(lists[types.index(a)])
        meanings = []
        for x in re.findall(r'\((.*?)\)', reg):
            if 'often followed by' in x:
                pass
            elif len(x) > 5 or ' ' in str(x):
                meanings.append(x)
        name = a.text
        out[name] = meanings
    return out
