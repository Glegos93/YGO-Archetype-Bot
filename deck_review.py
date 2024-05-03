import requests
import math


def get_card_ids(archetype):
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?archetype={archetype}'
    response = requests.get(url)
    data = response.json()

    card_ids = [card['id'] for card in data['data']]

    print(card_ids)
    return card_ids


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
