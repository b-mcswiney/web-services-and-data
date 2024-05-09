import nltk
import json
from list import list_pages
from build import build_index


nltk.download("punkt")
nltk.download("stopwords")

def load_index():

    try:
        f = open("index.json", "r")

        data = json.load(f)
    except Exception as e:
        print("Error loading index. Returning empty index. Use 'build' to build index.")
        print(e)
        return {"terms": {}, "doc-map": {}}

    print("Index loaded successfully")
    
    return data


def print_index(word: str, index: dict, urls: dict):
    if word not in index:
        print("Word not found in index")
        return

    print("------------------------------------------------------------------------")
    print("Frequency index for:", word)
    print("------------------------------------------------------------------------")

    print_count = 3
    for doc in index[word]:
        print("[",  urls[str(doc["doc-id"])],":", doc["frequency"], "]")
        if print_count % 10 == 0 and print_count != 0:
            print("Continue? (Y/n)")
            cont = input()
            if cont == "n":
                break
        print_count += 1
    
    print("------------------------------------------------------------------------")
    print("positions for:", word)
    print("------------------------------------------------------------------------")
    print_count = 3
    for doc in index[word]:
        print("[", urls[str(doc["doc-id"])], ":", doc["locations"], "]")
        if print_count % 10 == 0 and print_count != 0:
            print("Continue? (Y/n)")
            cont = input()
            if cont == "n":
                break
        print_count += 1

def main():
    input_prompt = "\n\n>> "
    urls = []
    index = {"terms": {}, "doc-map": {}}
    index_default = {"terms": {}, "doc-map": {}}

    while True:
        print(input_prompt, end="")

        # Get user input
        user_input = input()

        input_list = user_input.split(" ")

        if input_list[0] == "exit":
            break

        elif input_list[0] == "build":
            if index == index_default:
                urls, index = build_index("https://quotes.toscrape.com", urls, index)
                # print(index)
            else:
                print("Index already built")

        elif input_list[0] == "load":
            index = load_index()

        elif input_list[0] == "print" and index != index_default:
            if len(input_list) < 2:
                print("No word given")
                continue
            if len(input_list) > 2:
                print("Too many words given")
                continue

            print_index(input_list[1], index["terms"], index["doc-map"])

        elif input_list[0] == "find" and index != index_default:
            input_list.remove("find")
            if len(input_list) == 0:
                print("No search terms given")
                continue

            list_pages(input_list, index["terms"], index["doc-map"])

        elif input_list[0] == "help":
            print("Commands:")
            print("  Build - Build the index")
            print("  Load - Load the index from file (requires Build)")
            print("  Print [word] - Print inverted index for given word")
            print("  Search [terms] - Gives pages where terms appear")
            print("  exit - Exit the program")

        elif input_list[0] not in ["build", "load", "print", "find", "help", "exit"]:
            print("Invalid command. Type 'help' for a list of commands")

        else:
            print("No index built. Type 'build' or 'load' to build index")

main()