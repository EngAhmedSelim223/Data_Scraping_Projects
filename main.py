# this is a script to make a file with the name of each movie on https://subslikescript.com/ and scraping the transcript of the movie
# to this file 
import requests
from bs4 import BeautifulSoup

links = []
for i in range(1,100):
    website = f"https://subslikescript.com/movies?page={i}"
    resonse = requests.get(website)
    content = resonse.text
    soup = BeautifulSoup(content, "lxml")
    box = soup.find("article", {"class": "main-article"})
    for link in box.find_all("a"):
        links.append(f"https://subslikescript.com/{link['href']}")


for link in links:
    try:

        response = requests.get(link)
        content = response.text
        soup = BeautifulSoup(content, "lxml")
        box = soup.find("article", {"class": "main-article"})
        title = box.find("h1").get_text().strip()
        transcript = box.find("div", {"class": "full-script"}).get_text(separator='\n')
        with open(f"{title}.txt", "w", encoding="UTF-8") as file:
            file.write(transcript)
    except:
        print(f"there is a problem with {title}")
