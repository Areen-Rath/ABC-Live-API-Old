import time
import requests
from bs4 import BeautifulSoup
import lxml
from concurrent.futures import ThreadPoolExecutor
import time

session = requests.Session()
def th_fetch():
    data = session.get("https://www.thehindu.com/business/markets/")
    soup = BeautifulSoup(data.content, "lxml")
    time.sleep(0.01)

    links = []
    titles = []
    descs = []
    imgs = []

    a_data = soup.find(class_ = "row xs-reverse two-thr-one sub-sections equal-height")
    a_tags = a_data.find_all("a")
    for a in a_tags:
        try:
            if a.text:
                links.append(a["href"])
                titles.append(a.text.replace("\n", "").replace("\t", "").strip())
        except:
            continue
    
    with ThreadPoolExecutor(max_workers = len(links)) as p:
        future = list(p.submit(scrape_more, link).result() for link in links)

    for i in future:
        descs.append(i[0])
        imgs.append(i[1])

    data = []
    for index, link in enumerate(links):
        if descs[index] and imgs[index]:
            data.append({
                "title": titles[index],
                "desc": descs[index],
                "link": links[index],
                "img": imgs[index]
            })

    return data

def scrape_more(link):
    desc_img = []

    article = session.get(link)
    article_soup = BeautifulSoup(article.content, "lxml")

    desc = article_soup.find("h2", attrs = {"class", "sub-title"})
    if not desc:
        desc_img.append(None)
    else:
        desc_img.append(desc.text)

    img = article_soup.find("source")
    if not img:
        desc_img.append(None)
    else:
        desc_img.append(img["srcset"])

    return desc_img

print(th_fetch())