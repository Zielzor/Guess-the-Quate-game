import requests
from random import choice
from csv import DictReader
from bs4 import BeautifulSoup

URL = 'http://quotes.toscrape.com/'

def read_quotes(filename):
    with open (filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

def start_playing(function):
    quote = choice(whole_set)
    guesses_left = 4
    print("Who said this quote?")
    print(quote["text"])
    print(quote["author"]) # For testing purposes
    guess = ""

#logic
    while guess.lower() != quote["author"].lower():
        guess = input(f"Who said that? {guesses_left} guesses remain:> " )
        guesses_left-= 1
        if guess.lower() == quote["author"].lower():
            print("Gratz, you guessed!")
            guesses_left -= 1
            break
        elif guesses_left == 3:
            res = requests.get(f"{URL}{quote['author bio']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Hint 1 : Author was born in {birth_date} {birth_place}")
        elif guesses_left == 2:
            first_letter = quote["author"][0]
            print(f"Hint 2 : Author's name starts with {first_letter}")
        elif guesses_left == 1:
            second_name_1st_letter = quote['author'].split(" ")[1][0]
            print(f"Hint 3 : Author's last name starts with {second_name_1st_letter}")

        else:
            print(f"You failed, the answer was {quote['author']}")
            break

    again = ""
    while again.lower() not in ('y', 'yes','n','no'):
        again = input("Would you like to play again? (y/n) :>")
        if again.lower() in ('yes','y'):
            print("Alright, go on")
            start_playing(whole_set)
        else:
            print("Alright, bye")

whole_set = read_quotes("quotes.csv")
start_playing(whole_set)