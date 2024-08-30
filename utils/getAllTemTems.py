import requests
from random import randint
from bs4 import BeautifulSoup as bs

def getRandomHeaders():
            with open ("user_agents.txt", "r") as file:
                file_content = file.readlines()
            user_agents = [x.strip() for x in file_content]
            user_agent = user_agents[ randint(0,len(user_agents)) ] #select random agent
            return {"User-Agent": user_agent}

def getAllTemtemsPage():
    html = requests.get('https://temtem.fandom.com/wiki/Temtem_(creatures)', headers=getRandomHeaders() ).content
    return html

def getAllTemTems():
    temtems = []
    html = getAllTemtemsPage()

    soup = bs(html, "lxml")
    infobox = soup.find('table')

    # Loop through all links in the infobox
    for link in infobox.find_all('a'):
        if 'title' in link.attrs and 'type' not in link.attrs['title'].lower():
            temtems.append(link.get('title'))

    return temtems