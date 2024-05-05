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
        html = requests.get(u)

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

        # if count == 4:
        #     break
        count += 1
    
    dump_index(index)
    
    return urls, index


def parse_tokens(tokens: list, document: int, index: dict):
    count = 0

    # Add locations to index
    for t in tokens:
        token = t.lower()
        if len(token) > 1:
            if token not in index:
                index[token] = {}
                index[token]["doc-id"] = [document]
                index[token]["locations"] = [count]
            else:
                if document not in index[token]["doc-id"]:
                    index[token]["doc-id"].append(document)
                    index[token]["locations"].append(count)
                else:
                    index[token]["locations"].append(count)
        count += 1

    for i in index:
        index[i]["frequency"] = len(index[i]["locations"])


    return index


def dump_index(index: dict):
    with open("index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "Index dumped to index.txt"
