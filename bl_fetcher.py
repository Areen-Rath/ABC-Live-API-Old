import requests
from selectolax.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
def bl_fetch():
    data = requests.get("https://www.thehindubusinessline.com/")
    parsed = HTMLParser(data.text)

    titles = []
    links = []
    descs = []
    imgs = []

    a_data = parsed.css("div.after-border-right")
    for a in a_data[0].css("a"):
        try:
            if (
                a.attributes["href"] not in links
                and a.text()
                and a.attributes["href"][36:42] != "/news/"
                and a.attributes["href"][-4:] == ".ece"
            ):
                links.append(a.attributes["href"])
                titles.append(a.text())
        except:
            continue

    for a in a_data[1].css("a"):
        try:
            if (
                a.attributes["href"] not in links
                and a.text()
                and a.attributes["href"][36:42] != "/news/"
                and a.attributes["href"][-4:] == ".ece"
            ):
                links.append(a.attributes["href"])
                titles.append(a.text())
        except:
            continue

    for a in a_data[0].css("a"):
        try:
            if (
                a.attributes["href"] not in links
                and a.text()
                and a.attributes["href"][36:42] != "/news/"
                and a.attributes["href"][-4:] == ".ece"
            ):
                links.append(a.attributes["href"])
                titles.append(a.text())
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

        desc = article_parsed.css_first("h2.sub-title")
        if len(desc.text()) <= 100:
            desc_img.append(desc.text().replace("\n", "").strip())
        else:
            desc_img.append(f"{desc.text().replace("\n", "").strip()[:100]}...")

        try:
            img = article_parsed.css_first("source")
            desc_img.append(img.attributes["srcset"])
        except:
            desc_img.append("https://raw.githubusercontent.com/Areen-Rath/ABC-Live/refs/heads/main/assets/logo.png")
    except:
        desc_img = [None, None]

    return desc_img

print(bl_fetch())