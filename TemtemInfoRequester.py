import requests
from random import randint
from bs4 import BeautifulSoup as bs
import os

class TemtemInfoRequester:
    def __init__(self, temtem):
        self.temtem = temtem
        self.wiki_url = 'https://temtem.fandom.com/wiki/' + self.temtem
        self.html_file_path = f"temtems/{self.temtem}.html"

    def getAllInfo(self):
        self.html = self.getWikiPage()
        if self.html is not None:
            self.getTemtemImage()
            self.getType()
            self.getTypeMatchups()
            return {
                "name": self.temtem,
                "type": self.types,
                "image_url": self.temtem_image,
                "type_matchup": self.matchups,
            }
        return None

    def getRandomHeaders(self):
        with open("user_agents.txt", "r") as file:
            file_content = file.readlines()
        user_agents = [x.strip() for x in file_content]
        user_agent = user_agents[randint(0, len(user_agents) - 1)]  # select random agent
        return {"User-Agent": user_agent}

    def getWikiPage(self):
        # Check if the HTML file already exists
        if os.path.exists(self.html_file_path):
            with open(self.html_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            try:
                # Make the request and save the content to a file
                html_content = requests.get(self.wiki_url, headers=self.getRandomHeaders()).content
                os.makedirs(os.path.dirname(self.html_file_path), exist_ok=True)
                with open(self.html_file_path, 'wb') as file:
                    file.write(html_content)
                return html_content
            except Exception as e:
                print(f"Error fetching wiki page: {e}")
                return None

    def getTemtemImage(self):
        soup = bs(self.html, "lxml")
        infobox = soup.find(class_="infobox temtem")

        if infobox is not None:
            for link in infobox.find_all('a'):
                try:
                    img_tag = link.find('img')
                    if img_tag and img_tag['alt'].lower() == self.temtem.lower():  # Check if alt matches temtem name
                        image_url = img_tag.get('data-src')  # Get the data-src attribute
                        if image_url:
                            self.temtem_image = image_url
                            return
                except Exception as e:
                    print(f"Error: {e}")
                    continue

        self.temtem_image = None
        return

    def getType(self):
        self.types = []
        soup = bs(self.html, "lxml")
        infobox = soup.find(class_="infobox temtem")

        # Loop through all links in the infobox
        for link in infobox.find_all('a'):
            # Check if 'title' attribute exists and contains 'type'
            if 'title' in link.attrs and 'type' in link.attrs['title'].lower():
                self.types.append(link.get('title')[:-5])

    def getTypeMatchups(self):
        soup = bs(self.html, "lxml")
        type_table = soup.find(class_="type-table")

        temtem_types = []
        for link in type_table.find_all('a'):
            temtem_type = link.attrs['title'][:-5]
            temtem_types.append(temtem_type)

        multipliers = []
        for entry in type_table.find_all(class_=lambda x: x and 'resist' in x):
            multipliers.append(entry.text.strip())

        self.matchups = {}
        for type, multiplier in zip(temtem_types, multipliers):
            self.matchups[type] = multiplier

# USAGE:
if __name__ == '__main__':
    temtem = 'Saku'
    requester = TemtemInfoRequester(temtem)
    data = requester.getAllInfo()
    print(data)
