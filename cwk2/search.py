import nltk
from list import list_pages
from build import build_index

nltk.download("punkt")


def load_index():
    return "not implemented"


def print_index(word: str, index: dict):
    return index[word]


def main():
    input_prompt = "\n\n>> "
    urls = []
    index = {"terms": {}, "doc-map": {}}

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
            load_index()

        if input_list[0] == "print":
            print(print_index(input_list[1]), index)

        if input_list[0] == "find":
            input_list.remove("find")
            list_pages(input_list, index, urls)

        if input_list[0] == "help":
            print("Commands:")
            print("  Build - Build the index")
            print("  Load - Load the index from file (requires Build)")
            print("  Print [word] - Print inverted index for given word")
            print("  Search [terms] - Gives pages where terms appear")
            print("  exit - Exit the program")


main()