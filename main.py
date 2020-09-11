import requests
from bs4 import BeautifulSoup
from time import sleep 

URL = 'http://quotes.toscrape.com/'
page_url = "/page/1"
whole_set = []


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

print(whole_set)