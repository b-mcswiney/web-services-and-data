import nltk
import json
from list import list_pages
from build import build_index


nltk.download("punkt")
nltk.download("stopwords")

def load_index():

    f = open("index.json", "r")

    data = json.load(f)

    return data


def print_index(word: str, index: dict, urls: dict):
    if word not in index:
        print("Word not found in index")
        return

    print("Frequency index for:", word)
    print("------------------------------------------------------------------------")
    for doc in index[word]:
        print("[",  urls[str(doc["doc-id"])],":", doc["frequency"], "]")
    
    print("positions for:", word)
    print("------------------------------------------------------------------------")
    for doc in index[word]:
        print("[", urls[str(doc["doc-id"])], ":", doc["locations"], "]")


def main():
    input_prompt = "\n\n>> "
    urls = []
    index = {"terms": {}, "doc-map": {}}

    stopwords = nltk.corpus.stopwords.words("english")
    print(stopwords)

    while True:
        print(input_prompt, end="")

        # Get user input
        user_input = input()

        input_list = user_input.split(" ")

        if input_list[0] == "exit":
            break

        if input_list[0] == "build":
            if index == {"terms": {}, "doc-map": {}}:
                urls, index = build_index("https://quotes.toscrape.com", urls, index)
                # print(index)
            else:
                print("Index already built")

        if input_list[0] == "load":
            index = load_index()

        if input_list[0] == "print":
            print_index(input_list[1], index["terms"], index["doc-map"])

        if input_list[0] == "find":
            input_list.remove("find")
            list_pages(input_list, index["terms"], index["doc-map"])

        if input_list[0] == "help":
            print("Commands:")
            print("  Build - Build the index")
            print("  Load - Load the index from file (requires Build)")
            print("  Print [word] - Print inverted index for given word")
            print("  Search [terms] - Gives pages where terms appear")
            print("  exit - Exit the program")


main()