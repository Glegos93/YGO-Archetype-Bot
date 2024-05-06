import requests
import math
import requests
from bs4 import BeautifulSoup


def count_cards(user_deck, archetype_deck):
    match_counter = 0
    count = 0
    for card in user_deck:
        count += 1
        if card in archetype_deck:
            match_counter += 1

    percentage = 0
    if count > 0:
        percentage = math.ceil((match_counter / count) * 100)

    print(f"Matched cards: {match_counter}")
    print(f"Total deck size: {count}")
    print(f"Percentage of matched cards: {percentage}%")
    return percentage


def scrape_yugipedia(archetype):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f'https://yugipedia.com/wiki/{archetype}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    yugipedia_archetype_cards = []
    for group in soup.find_all(class_='smw-row'):
        for a in group.find_all('a'):
            title = a.get('title')
            if title:
                yugipedia_archetype_cards.append(title)
    return yugipedia_archetype_cards


def scrape_yugioh_archetype(archetype):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f'https://www.yugiohcardguide.com/archetype/{archetype}.html', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    yugioh_archetype_cards = []
    card_data_table = soup.find(id='card_data')
    if card_data_table:
        tbody = card_data_table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                td = tr.find('td')
                if td:
                    a_tag = td.find('a')
                    if a_tag:
                        b_tag = a_tag.find('b')
                        if b_tag:
                            yugioh_archetype_cards.append(b_tag.get_text(strip=True))
    return yugioh_archetype_cards
