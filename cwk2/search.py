
def build_index():
    return "not implemented"

def load_index():
    return "not implemented"

def print_index(word: str):
    return "not implemented"

def list_pages(terms: list):
    return "not implemented"

def main():
    input_prompt = ">> "
    while True:
        print(input_prompt, end="")

        # Get user input
        user_input = input()

        input_list = user_input.split(" ")

        if input_list[0] == "exit":
            break

        if input_list[0] == "build":
            build_index()

        if input_list[0] == "load":
            load_index()

        if input_list[0] == "print":
            print_index(input_list[1])

        if input_list[0] == "find":
            list_pages(input_list)

        if input_list[0] == "help":
            print("Commands:")
            print("  Build - Build the index")
            print("  Load - Load the index from file (requires Build)")
            print("  Print [word] - Print inverted index for given word")
            print("  Search [terms] - Gives pages where terms appear")
            print("  exit - Exit the program")


main()