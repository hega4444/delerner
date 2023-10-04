import sqlite3
import os
import random
import time
import json
from article_reader import extract_words_from_webpage
from translator import translate_en_de, translate_de_en
from key import get_key

def clear_screen():
    # Clear the screen based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-like systems (Linux, macOS)
        os.system('clear')

class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

def textcl(text, color):
    return f"{color}{text}{Color.RESET}"

def read_and_sort_dictionary(filename):
    # Connect to the SQLite database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Execute a query to retrieve data from a table
    cursor.execute('SELECT * FROM simple_translation')
    dictionary = cursor.fetchall()


    # Sort the list in descending order based on the third element of each tuple
    dictionary = sorted(dictionary, key=lambda x: x[3] if isinstance(x[3], float) else 0, reverse=True)

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return dictionary

def lookup(dictionary: list, word: str) -> str:
    for w in dictionary:
        if w[0].lower() == word.lower():
            return w
    return None

def get_list_words(dictionary, lastindex, nwords):
    return dictionary[lastindex:lastindex+nwords]

def play_cards(this_cards):

    guessed_word = 0
    cards = this_cards
    discard_these = []
    points = len(cards) * [0]
    level_complete = False
    last_word = 0

    while not level_complete:
        clear_screen()
        chosen_cards = random.sample(range(0, len(cards)), 4)

        while chosen_cards[0] in discard_these or chosen_cards[0] == last_word:
            chosen_cards = random.sample(range(0, len(this_cards)), 4)
        last_word = chosen_cards[guessed_word]

        guess = cards[chosen_cards[guessed_word]][0]
        print(textcl(f'{guess}', Color.BLUE))

        to_show = [this_cards[chosen_cards[x]][1] for x in range(1, 4)]
        answer = random.randint(0,2)
        to_show[answer] = cards[chosen_cards[guessed_word]][1]

        for i, option in enumerate(to_show):
            text = option
            print(textcl(f'{i+1}: {text}', Color.GREEN))
        
        print(textcl('Your answer:', Color.GREEN), end='', flush=True)
        user_input = get_key()
        clear_screen()
        try:
            user_input = int(user_input)
        except Exception:
            if isinstance(user_input, str):
                if user_input.lower() == 'q':
                    exit()
                elif user_input.lower() == 's':
                    return None
                #special command to skip the deck
                elif user_input.lower() == 'x':
                    return cards
                else:
                    user_input = -1

        if user_input-1 != answer:
            print(textcl(f"Correct answer: {cards[chosen_cards[guessed_word]][1]}.", Color.RED))
            time.sleep(1)
        else:
            print(textcl("Correct.", Color.GREEN))
            points[chosen_cards[guessed_word]] += 1
            if points[chosen_cards[guessed_word]] == 2 and len(cards) > 4:
                discard_these.append(chosen_cards[guessed_word])
            time.sleep(0.5) 

        if all(p >=1 for p in points):
            level_complete = True

    return this_cards
            

def cards_game(dictionary, loadFile = False):

    file_path = "data.json"
    loaded_data = {}
    words = {}
    words['trained'] = []
    lastindex = 0
    level = 0

    if loadFile:
        try:
            # Load the JSON data from the file
            with open(file_path, 'r') as json_file:
                loaded_data = json.load(json_file)
            print('Loading user history...')
            level = loaded_data['level']
            print(f'Level: {level}.')
            lastindex = loaded_data['index']
            words['trained'] = loaded_data['trained']
            time.sleep(0.5)

        except FileNotFoundError:
            lastindex = 0
            level = 0

    nwords = 10

    next = 'y'
    while next == 'y':

        if cards:=play_cards(get_list_words(dictionary, lastindex, nwords)):
            words['trained'].extend(cards)
            lastindex += nwords
            level += 1

        print('Next level? [y/n] :', end='', flush=True)
        next = get_key()
        if next.lower() == "y":  
            if level % 2 == 0:
                clear_screen()
                print(textcl('Recap level...', Color.BLUE))
                time.sleep(0.5)
                play_cards(random.sample(words['trained'], nwords))
                print('Next level? [y/n] :', end='', flush=True)
                next = get_key()
        else:
            next = 'no'
    
    print(f'You reached level: {level}.')

    #on exit
    if loadFile:
        data = {}
        data['level'] = level
        data['index'] = lastindex
        data['trained'] = words['trained']
        
        # Write the dictionary to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

def read_article(dictionary):
    clear_screen()
    url = input('Enter an URL to analize:')
    words_in_article = extract_words_from_webpage(url)
    words_in_article = [w for w in words_in_article if len(w) > 4]
    print('Creating vocabulary...')
    vocabulary = []

    if not words_in_article:
        print('Article could not be read. Try again...')
        time.sleep(0.5)
        return
    
    for w in words_in_article:
        if l:=lookup(dictionary, w):
            vocabulary.append(l)
    vocabulary = sorted(vocabulary, key=lambda x: x[3] if isinstance(x[3], float) else 10, reverse=False)
    cards_game(vocabulary, loadFile=False)
        
def translate_menu(lang):
    clear_screen()
    print('Enter your expressions. Enter to exit.')
    to_translate = " "
    while to_translate != "" and to_translate != "q":
        to_translate = input(f':{"E" if lang == "DE" else "D"}:')

        if lang == 'DE':
            print(textcl(':D:', Color.BLUE), textcl(translate_en_de(to_translate), Color.GREEN))
        elif lang == 'EN':
            print(textcl('Translation:', Color.BLUE), textcl(translate_de_en(to_translate), Color.GREEN))


def main():
    dictionary = read_and_sort_dictionary('de-en.sqlite3')

    while True:
        clear_screen()
        print(textcl('De-Lerner', Color.RED))
        print(textcl('1. General cards', Color.YELLOW))
        print(textcl('2. Train specific vocabulary with Article Reader', Color.YELLOW))
        print(textcl('3. Translate to DE', Color.YELLOW))
        print(textcl('4. Translate to EN', Color.YELLOW))
        print(textcl('5. Exit', Color.YELLOW))
        print('Select an option:', end='', flush=True)
        option = get_key()
        if option == '1':
            cards_game(dictionary, loadFile=True)
        elif option == '2':
            read_article(dictionary)
        elif option == '3':
            translate_menu('DE')
        elif option == '4':
            translate_menu('EN')
        elif option == '5':
            print()
            break


if __name__ == "__main__":
    main()