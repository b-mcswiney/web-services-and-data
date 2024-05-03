import time
from bs4 import BeautifulSoup
import requests
import nltk


def build_index(url: str, urls: list, index: dict):
    urls.append(url)

    count = 1
    for u in urls:
        # Print current scraping target
        print("-------------------------------------------------------------------")
        print("SCRAPING - ", u)
        print("-------------------------------------------------------------------")

        # politeness window between requests
        time.sleep(6)
        html = requests.get(u)

        # Convert request into soup
        soup = BeautifulSoup(html.text, "html.parser")

        # Find all links
        links = soup.find_all("a")

        # Add new links to urls list
        for link in links:
            if url + link.get("href") not in urls and link.get("href") != "/":
                urls.append(url + link.get("href"))

        # Get body of text
        body = soup.find("body")
        text = body.get_text()

        # Tokenize body
        tokens = nltk.word_tokenize(text)

        # Parse tokens
        index = parse_tokens(tokens, count, index)

        # Only get from a small about of pages
        count += 1
        if count == 4:
            break

    return urls, index


def parse_tokens(tokens: list, document: int, index: dict):

    # Add locations to index
    for t in tokens:
        token = t.lower()
        if len(token) > 1:
            if token not in index:
                index[token] = [document]
            else:
                if document not in index[token]:
                    index[token].append(document)

    return index
