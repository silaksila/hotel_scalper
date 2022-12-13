from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 '
            'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

hotels = pd.DataFrame({'Name': [], 'location': [], 'email': []})

hotel_list_URl = 'https://www.myswitzerland.com/en/accommodations/hotel-search/'

for i in range(1, 96):
    if i == 1:
        url = hotel_list_URl
    else:
        url = f'{hotel_list_URl}?p={i}'
    list_hotel_webpage = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(list_hotel_webpage.content, "lxml")
    hotel_list = soup.find_all(attrs={"class": "OfferTeaser grid"})

    for instance in hotel_list:

        name = instance.a['title'][22:]
        # remove + char and one space
        if '+' in name:
            name.replace('+', '')
            name = name[1:]

        # location
        location = instance.find('span', attrs={"class": "OfferTeaser--category"})
        location = location.string.strip()

        hotel_url = instance.a['href']
        h_webpage = requests.get(hotel_url, headers=HEADERS)
        hotel = BeautifulSoup(h_webpage.content, "lxml")

        # email
        email = hotel.find('a', attrs={'title': "Email"})
        if email:
            email = email['href']
            email = email[7:]

        # write data
            hotels.loc[len(hotels)] = (name, location, email)
        else:
            hotels.loc[len(hotels)] = (name, location, "null")
    print(i)

hotels.to_csv("database.csv")
print("Done")

