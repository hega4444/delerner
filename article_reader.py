import requests
from bs4 import BeautifulSoup
import re

def extract_words_from_webpage(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to fetch the webpage.')
        return []

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the HTML
    text = soup.get_text()

    # Tokenize text into words
    words = re.findall(r'\b\w+\b', text)

    return list(set(words))


