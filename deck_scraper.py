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
        side = deck_dict.get('side', [])

        combined_deck = main + extra + side

        print(combined_deck)

        return combined_deck

    return None
