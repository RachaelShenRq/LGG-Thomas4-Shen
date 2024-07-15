import requests
from bs4 import BeautifulSoup
import re
import json

def get_first_paragraph(wikipedia_url, session):
    wikipedia_response = session.get(wikipedia_url)
    soup = BeautifulSoup(wikipedia_response.text, 'html.parser')
    first_paragraph = ''
    for paragraph in soup.find_all('p'):
        if paragraph.find('b'):
            first_paragraph = paragraph.get_text()
            break
    first_paragraph = re.sub(r' \[.*\].*?,', ',', first_paragraph)
    return first_paragraph

def get_leaders():
    
    root_url = 'https://country-leaders.onrender.com'
    status_url = 'https://country-leaders.onrender.com/status' 
    cookie_url = "https://country-leaders.onrender.com/cookie"
    countries_url = "https://country-leaders.onrender.com/countries" 
    leaders_url = "https://country-leaders.onrender.com/leaders"


    cookies = requests.get(cookie_url).cookies

    countries = requests.get(countries_url, cookies=cookies).json()
  
    leaders_per_country = {}
    session_render = requests.Session()
    session_wikipedia = requests.Session()

    for country in countries:
        print(country)
        leaders_response = requests.get(leaders_url, cookies=cookies, params={'country': country})
        if leaders_response.status_code == 200:
            leaders_per_country[country] = leaders_response.json()
        else:
            print('new cookie')
            cookies = requests.get(cookie_url).cookies
            leaders_per_country[country] = session_render.get(leaders_url, cookies=cookies, params={'country': country}).json()

        for leader in leaders_per_country[country]:
            wikipedia_url = leader['wikipedia_url']
            leader['first_paragraph'] = get_first_paragraph(wikipedia_url, session_wikipedia)

    return leaders_per_country

def save(leaders_per_country):
    with open('leaders.json', 'w') as f:
        json.dump(leaders_per_country, f)

if __name__== "__main__"
    leaders_per_country = get_leaders()
    print(leaders_per_country)
    save(leaders_per_country)

    with open('leaders.json') as f :
        leaders_per_country_copy = json.load(f)
    print(leaders_per_country_copy == leaders_per_country)    