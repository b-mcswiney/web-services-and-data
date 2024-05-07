import time
from bs4 import BeautifulSoup
import requests
import nltk
import json


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

        # Get html from url
        html = requests.get(u)

        if html.status_code != 200:
            print("Failed to get page", u)
            continue

        # Convert request into soup
        soup = BeautifulSoup(html.text, "html.parser")

        # Find all links
        links = soup.find_all("a")

        # Add new links to urls list
        for link in links:
            if url + link.get("href") not in urls and link.get("href") != "/" and "http" not in link.get("href"):
                urls.append(url + link.get("href"))

        # Get body of text
        body = soup.find("body")
        text = body.get_text()

        # Tokenize body
        tokens = nltk.word_tokenize(text)

        # Parse tokens
        index["terms"] = parse_tokens(tokens, count, index["terms"])

        # add document to map
        index["doc-map"][str(count)] = u

        count += 1
    
    dump_index(index)
    
    return urls, index


def parse_tokens(tokens: list, document: int, index: dict):
    count = 0

    # Add locations to index
    for t in tokens:
        token = t.lower()
        if len(token) > 1 and token not in nltk.corpus.stopwords.words("english"):
            if token not in index:
                index[token] = []
                to_add = {"doc-id": document, "locations": [count], "frequency": 1}
                index[token].append(to_add)
            else:
                found = False
                for doc in index[token]:
                    if doc["doc-id"] == document:
                        doc["locations"].append(count)
                        doc["frequency"] += 1
                        found = True
                if not found:
                    to_add = {"doc-id": document, "locations": [count], "frequency": 1}
                    index[token].append(to_add)
        count += 1

    return index


def dump_index(index: dict):
    with open("index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "Index dumped to index.txt"
