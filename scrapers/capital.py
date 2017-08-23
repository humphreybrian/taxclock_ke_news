import json

from .base import Scraper
from .config import scrape_sites, base_urls


class CapitalMedia(Scraper):
    def __init__(self):
        super(CapitalMedia, self).__init__()
        self.url = scrape_sites["capital"]
        self.base = Scraper()

    def scrape_page(self):
        result_html = self.base.get_html_content(self.url)
        if result_html:
            data = []
            items = result_html.find_all("div", class_="article-wrapper")
            print(items)
            for item in items:
                img_url = item.find("img").get("src")
                link = item.find("a").get("href")
                text = item.find("h2").text
                data.append({
                    'link': link,
                    'img': img_url,
                    'title': text
                })
            print (json.dumps(data, indent=2))
            self.base.s3.put_object(
                Bucket='taxclock.codeforkenya.org',
                ACL='public-read',
                Key='data/standard-news.json',
                Body=json.dumps(data)
            )
        else:
            print "The ideal html content could not be retrieved."
