import time
import requests
from requests import Session
from bs4 import BeautifulSoup
import lxml
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
def mc_fetch():
    data = requests.get("https://www.moneycontrol.com/")
    soup = BeautifulSoup(data.content, "lxml")
    time.sleep(0.01)

    links = []
    titles = []
    descs = []
    imgs = []

    a_data = soup.find(class_ = "sub-col-left")
    a_tags = a_data.find_all("a")
    for a in a_tags:
        if (
            a["href"] not in links
            and a["href"][28:43] == "/news/business/"
            and a["href"][42:51] != "/markets/"
            and a["href"][42:55] != "/commodities/"
        ):
            links.append(a["href"])
            titles.append(a["title"])

    a_data = soup.find(class_ = "sub-col-rht")
    a_tags = a_data.find_all("a")
    for a in a_tags:
        if (
            a["href"] not in links
            and a["href"][28:43] == "/news/business/"
            and a["href"][42:51] != "/markets/"
            and a["href"][42:55] != "/commodities/"
            and a["href"][42:53] != "/companies/"
        ):
            links.append(a["href"])
            titles.append(a["title"])
            
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
                "link": link,
                "img": imgs[index]
            })

    return data

def scrape_more(link):
    desc_img = []

    article = session.get(link)
    article_soup = BeautifulSoup(article.content, "lxml")

    desc = article_soup.find("h2", attrs = {"class", "article_desc"})
    if not desc:
        desc_img.append(None)
    else:
        desc_img.append(desc.text)

    img_data = article_soup.find(class_ = "article_image")
    if not img_data:
        desc_img.append(None)
    else:
        try:
            img = img_data.find_all("img")
            desc_img.append(img[0]["data-src"])
        except:
            desc_img.append(None)

    return desc_img