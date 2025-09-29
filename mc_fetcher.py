import requests
from selectolax.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
def mc_fetch():
    data = requests.get("https://www.moneycontrol.com/")
    parsed = HTMLParser(data.text)

    titles = []
    links = []
    descs = []
    imgs = []

    a_left = parsed.css("div.sub-col-left")
    a_rht = parsed.css("div.sub-col-rht")
    for a in a_left[0].css("a"):
        if (
            a.attributes["href"] not in links
            and a.text() != "MC EXCLUSIVE"
            and a.attributes["href"][28:43] == "/news/business/"
            and a.attributes["href"][42:55] != "/commodities/"
        ):
            links.append(a.attributes["href"])
            titles.append(a.text().replace("\n", "").replace("\t", ""))
    
    for a in a_left[1].css("a"):
        try:
            if (
                a.attributes["href"] not in links
                and a.text() != "MC EXCLUSIVE"
                and a.attributes["href"][28:43] == "/news/business/"
                and a.attributes["href"][42:55] != "/commodities/"
            ):
                links.append(a.attributes["href"])
                titles.append(a.text().replace("\n", "").replace("\t", ""))
        except:
            continue

    for a in a_rht[0].css("a"):
        try:
            if (
                a.attributes["href"] not in links
                and a.text() != "MC EXCLUSIVE"
                and a.attributes["href"][28:43] == "/news/business/"
                and a.attributes["href"][42:55] != "/commodities/"
            ):
                links.append(a.attributes["href"])
                titles.append(a.text().replace("\n", "").replace("\t", ""))
        except:
            continue

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
    try:
        desc_img = []
        article = session.get(link)
        article_parsed = HTMLParser(article.text)

        desc = article_parsed.css_first("h2.article_desc")
        if len(desc.text()) <= 100:
            desc_img.append(desc.text())
        else:
            desc_img.append(f"{desc.text()[:100]}...")

        try:
            img = article_parsed.css_first("div.article_image").css_first("img")
            desc_img.append(img.attributes["data-src"])
        except:
            desc_img.append("https://raw.githubusercontent.com/Areen-Rath/ABC-Live/refs/heads/main/assets/logo.png")
    except:
        desc_img = [None, None]

    return desc_img