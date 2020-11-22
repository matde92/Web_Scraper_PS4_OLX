from bs4 import BeautifulSoup
from requests import get
import pandas as pd

num=(1,2) #definiuje ilosc stron do przejrzenia

data=[["Location","Title","Price","Link"]] #tworze liste do ktorej dodawane beda wyniki wyszukiwan

for number in num: #petla ktora sprawdzi kolejno strony

    site=("https://www.olx.pl/elektronika/gry-konsole/konsole/podkarpackie/q-ps4/"+"?page="+str(number))

    page=get(site)
    
    bs= BeautifulSoup(page.content, "html.parser")

    for offer in bs.find_all('div', class_="offer-wrapper"): #petla ktora przejrzy oferty i wyciagnie przydatne informacje
        footer=offer.find('td', class_="bottom-cell")
        location=footer.find('small', class_="breadcrumb").get_text().strip().split(',')[0]
        title=offer.find('strong').get_text().strip()
        price=float((offer.find('p', class_="price")).get_text().strip().replace("zł","").replace(" ","").replace("Zamienię","0"))
        www=offer.find('a')['href']
        data.append([location,title,price,www])

column_names=data.pop(0) #wyodrebniam elementy listy ktore posluza jako naglowki

df=pd.DataFrame(data, columns=column_names).sort_values(by="Price",ascending=False).drop_duplicates(subset="Title",keep='first') #tworze DataFrame w pandas

df=df[(df['Price']<1000)&(df['Price']>350)] #dodaje zakresy cenowe
print(df)

