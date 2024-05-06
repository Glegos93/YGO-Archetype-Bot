import requests
from bs4 import BeautifulSoup
import re
import json


def scrape_decks(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    script_tag = None
    for script in soup.find_all('script'):
        if 'var Deck' in script.text:
            script_tag = script.text
            break

    if script_tag:
        deck_str = re.search(r'var Deck = ({.*?});', script_tag, re.DOTALL).group(1)
        deck_str = deck_str.replace("'", '"')  # replace single quotes with double quotes to make it valid JSON
        deck_dict = json.loads(deck_str)

        main = deck_dict.get('main', [])
        extra = deck_dict.get('extra', [])

        combined_deck = main + extra

        # Get card names
        card_info = get_card_names(combined_deck)
        card_id_to_name = {card['id']: card['name'] for card in card_info}

        # Replace IDs with names
        combined_deck = [card_id_to_name.get(card_id, card_id) for card_id in combined_deck]

        return combined_deck

    print("opps something went wrong")
    return None


def get_card_names(card_ids):
    card_info = []
    ids_string = ','.join(map(str, card_ids))  # Convert the list of IDs to a comma-separated string
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?id={ids_string}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and data['data']:
        for card in data['data']:
            card_info.append({'id': card['id'], 'name': card['name']})
    return card_info
