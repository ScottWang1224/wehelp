from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

with open("articles.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    url = "https://www.ptt.cc/bbs/Steam/index.html"
    headers={"User-Agent": "Mozilla/5.0"}

    for i in range(3):
        request = Request(url,headers=headers)
        response = urlopen(request)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("div", class_="r-ent")

        for article in articles:
            title_tag = article.find("div", class_="title").find("a")

            if title_tag is None:
                continue

            title = title_tag.text.strip()

            like = article.find("div", class_="nrec").text.strip()

            article_url = "https://www.ptt.cc" + title_tag["href"]
            article_request = Request(
            article_url,headers=headers)
            article_response = urlopen(article_request)
            article_html = article_response.read().decode("utf-8")

            article_soup = BeautifulSoup(article_html, "html.parser")

            meta_values = article_soup.find_all(
            "span",
            class_="article-meta-value"
            )

            if len(meta_values) > 0:
                publish_time = meta_values[-1].text.strip()
            else:
                publish_time = ""

            writer.writerow([
                title,
                like,
                publish_time
            ])
        paging = soup.find("div", class_="btn-group btn-group-paging")
        links = paging.find_all("a")
        previous_page = links[1]["href"]
        url = "https://www.ptt.cc" + previous_page

