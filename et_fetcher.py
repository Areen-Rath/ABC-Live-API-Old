import time
import requests
from bs4 import BeautifulSoup
import lxml
from concurrent.futures import ThreadPoolExecutor
import time

session = requests.Session()
def et_fetch():
    data = session.get("https://economictimes.indiatimes.com/markets")
    soup = BeautifulSoup(data.content, "lxml")
    time.sleep(0.01)

    links = []
    titles = []
    descs = []
    imgs = []

    a_data = soup.find(id = "topStories")
    a_tags = a_data.find_all("a")
    for a in a_tags:
        if a["href"][:21] == "/markets/stocks/news/":
            links.append(f"https://economictimes.indiatimes.com/{a["href"]}")
            titles.append(a.text)
    
    with ThreadPoolExecutor(max_workers = len(links)) as p:
        future = list(p.submit(scrape_more, link).result() for link in links)

    for i in future:
        descs.append(i[0])
        imgs.append(i[1])

    data = []
    for index, link in enumerate(links):
        if descs[index]:
            data.append({
                "title": titles[index],
                "desc": descs[index],
                "link": link,
                "img": imgs[index]
            })
    
    return data

def scrape_more(link):
    desc_img = []

    article = session.get(link)
    article_soup = BeautifulSoup(article.content, "lxml")

    desc = article_soup.find("h2", attrs = {"class", "summary"})
    if not desc:
        desc_img.append(None)
    else:
        sentences = desc.text.split(".")
        if len(sentences) >= 2:
            desc = f"{sentences[0]}.{sentences[1]}."
            desc_img.append(desc)
        else:
            desc_img.append(f"{sentences[0]}.")

    img = article_soup.find_all("img")
    desc_img.append(img[3]["src"])

    return desc_img