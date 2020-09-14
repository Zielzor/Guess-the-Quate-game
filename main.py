import requests
from bs4 import BeautifulSoup
from time import sleep 
from random import choice



URL = 'http://quotes.toscrape.com/'
whole_set = []

def get_quotes():
    page_url = "/page/1"
    while URL:
        headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        page = requests.get(f"{URL}{page_url}",headers)
        soup = BeautifulSoup(page.content, "html.parser")

        quote_text = soup.find_all(class_="quote")
        
        for q in quote_text:
            single_quote = q.find(class_="text").get_text()
            person_name = q.find(class_="author").get_text()
            author_bio = q.find("a")["href"]
            whole_set.append({
                "text":f"{single_quote}",
                "author":f"{person_name}",
                "author bio":f"{author_bio}"
            })
        
        next_page= soup.find(class_="next")
        if next_page:
            page_url = next_page.find("a")["href"]
            print(page_url)
        else:
            page_url = None
            break 
    

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
            start_playing(quotes)
        else:
            print("Alright, bye")
#start of the actual game
quotes= get_quotes()
start_playing(quotes)






