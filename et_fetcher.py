import requests
from selectolax.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
def et_fetch():
    data = requests.get("https://economictimes.indiatimes.com/markets")
    parsed = HTMLParser(data.text)

    links = []
    titles = []
    descs = []
    imgs = []

    a_data = parsed.css_first("div.topStories")
    for a in a_data.css("a"):
        try:
            if (
                a.attributes["href"][:9] == "/markets/"
                and a.attributes["href"][8:21] != "/expert-opinion/"
            ):
                links.append(f"https://economictimes.indiatimes.com{a.attributes['href']}")
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

        desc = article_parsed.css_first("h2.summary")
        if len(desc.text()) <= 100:
            desc_img.append(desc.text())
        else:
            desc_img.append(f"{desc.text()[:100]}...")

        try:
            img = article_parsed.css_first("figure.artImg").css_first("img")
            desc_img.append(img.attributes["src"])
        except:
            desc_img.append("https://raw.githubusercontent.com/Areen-Rath/ABC-Live/refs/heads/main/assets/logo.png")
    except:
        desc_img = [None, None]

    return desc_img