from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner
import extruct
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
from urllib.parse import urljoin
from algoliasearch.search_client import SearchClient
import json
import hashlib


with open("../secrets.json") as f:
    secrets = json.loads(f.read())

client = SearchClient.create(secrets['id'], secrets['key'])
index = client.init_index("dev_main")


def algolia_save(data, url):
    entry_id = hashlib.new('sha256')
    entry_id.update(url.encode())

    title = data['title']
    metadata = data['metadata']
    ld = metadata['json-ld']
    og = metadata['opengraph']
    description = data['text']
    favicon = data['icon']
    image = None

    if ld is not None and len(ld) > 0:
        if 'name' in ld[0]:
            title = ld[0]['name']
        if 'url' in ld[0]:
            url = ld[0]['url']
        if 'image' in ld[0]:
            image = ld[0]['image']

    if og is not None and len(og) > 0:
        ogp = og[0]['properties']
        title_item = next(filter(lambda x: x[0] == "og:title", ogp), None)
        description_item = next(filter(lambda x: x[0] == "og:description", ogp), None)
        url_item = next(filter(lambda x: x[0] == "og:url", ogp), None)
        image_item = next(filter(lambda x: x[0] == "og:image", ogp), None)

        if title_item is not None:
            title = title_item[1]
        if description_item is not None:
            description = description_item[1]
        if url_item is not None:
            url = url_item[1]
        if image_item is not None:
            image = image_item[1]

    sl = []

    for i in data['sublinks']:
        if i is None or i[0] is None or i[1] is None:
            continue
        if i[0].strip() == "" or i[1].strip() == "":
            continue
        sl.append({
            'label': i[0].strip(),
            'id': i[1].strip()
        })

    record = {
        "objectID": entry_id.hexdigest(),
        "title": title,
        "url": url,
        "image": image,
        "description": description,
        "icon": favicon
    }

    index.save_object(record)


def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link


class ImdbCrawler(CrawlSpider):
    name = 'main'
    start_urls = [
        'https://equestria.dev/',
        'https://ponycule.p.equestria.dev/',
        'https://source.equestria.dev/',
        'https://signaljs.equestria.dev/',
        'https://status.equestria.dev/',
        'https://en.wikipedia.org/',
        'https://youtube.com/',
        'https://twitter.com/',
        'https://reddit.com/',
        'https://reuters.com/',
        'https://kde.org/',
        'https://mozilla.org/',
        'https://google.com/',
        'https://derpibooru.org/',
        'https://furbooru.org/',
        'https://e621.net/',
        'https://wikimedia.org/',
        'https://stackoverflow.com/',
        'https://duckduckgo.com/',
        'https://android.com/',
        'https://apple.com/',
        'https://microsoft.com/',
        'https://amazon.com/',
        'https://redhat.com/',
        'https://github.com/',
        'https://gitlab.com/',
        'https://mastodon.social/',
        'https://jetbrains.com/',
        'https://flathub.org/',
        'https://fedora.org/',
        'https://ubuntu.com/',
        'https://facebook.com/',
        'https://instagram.com/',
        'https://yahoo.com/',
        'https://pornhub.com/',
        'https://linkedin.com/',
        'https://netflix.com/',
        'https://samsung.com/',
        'https://discord.com/',
        'https://quora.com/',
        'https://msn.com/',
        'https://fandom.com/',
        'https://mylittlepony.fandom.com/',
        'https://g5mlp.fandom.com/',
        'https://reddit.com/r/furry/',
        'https://reddit.com/r/mlp/',
        'https://wikifur.com/',
    ]
    rules = (
        Rule(
            process_links=process_links,
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True

        texts = soup.find_all('p', text=True)
        visible_texts = filter(tag_visible, texts)
        print(list(visible_texts))
        all_texts = u" ".join(t.strip() for t in visible_texts)

        icons = []
        headers = []

        for item in soup.find_all('link', attrs={'rel': re.compile("^(shortcut icon|icon)$", re.I)}):
            icons.append(urljoin(response.url, item.get('href')))

        for header in soup.find_all('h2'):
            elid = header.get('id')

            if elid is not None:
                headers.append((header.string, elid))

        obj = {
            'title': soup.find('title').string,
            'icon': icons[0] if len(icons) > 0 else None,
            'text': all_texts,
            'url': response.url,
            'sublinks': headers,
            'metadata': extruct.extract(
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }

        algolia_save(obj, response.url)

        return obj
