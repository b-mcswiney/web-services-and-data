import requests

def login(session, url, username, password):
    data = {
        "username": username,
        "password": password
    }

    response = session.post(url + "/api/login", data=data)

    response_body = response.json()

    print(response_body["message"])

    if response.status_code == 200:
        return url
    
    return ""
    
def logout(session, url):
    response = session.post(url + "/api/logout")

    response_body = response.json()

    print(response_body["message"])

def post(session, url, headline, category, region, details):
    response = session.post(url + "/api/stories", json={
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
    })

    response_body = response.json()

    print(response_body["message"])

def parse_news_options(command):
    options_dict = {}

    for option in command:
        if option.startswith("-"):
            option_parts = option.split("=")
            options_dict[option_parts[0][1:]] = option_parts[1]

    # Check if specific options are in dictionary
    if "id" not in options_dict:
        options_dict["id"] = "*"
    if "cat" not in options_dict:
        options_dict["cat"] = "*"
    if "reg" not in options_dict:
        options_dict["reg"] = "*"
    if "date" not in options_dict:
        options_dict["date"] = "*"

    return options_dict

def news(options):

    newssites = requests.get("http://newssites.pythonanywhere.com/api/directory/")

    possible_sites = newssites.json()

    if options["id"] != "*":
        for site in possible_sites:
            if site["agency_code"] == options["id"]:
                url = site["url"]

    # Build the request
    params = {
        "story_cat": options["cat"],
        "story_region": options["reg"],
        "story_date": options["date"]
    }

    news = requests.get(url + "/api/stories", params=params)

    news_body = news.json()

    if news.status_code == 200:
        print_news(news_body["stories"])
    else:
        print(news_body["message"])

def print_news(news):
    for story in news:
        print("ID: ", story["key"])
        print("HEADLINE: ", story["headline"])
        print("CATEGORY: ", story["story_cat"])
        print("REGION: ", story["story_region"])
        print("DATE: ", story["story_date"])
        print("AUTHOR: ", story["author"])
        print("DETAILS: \n", story["story_details"])
        print("\n")

def list_news_sites():
    newssites = requests.get("http://newssites.pythonanywhere.com/api/directory/")

    possible_sites = newssites.json()

    for site in possible_sites:
        print("ID: ", site["agency_code"])
        print("URL: ", site["url"])
        print("NAME: ", site["agency_name"])
        print("\n")

def delete(session, url, id):
    response = session.delete(url + "/api/stories/" + str(id))

    response_body = response.json()

    print(response_body["message"])

def display_help():
    print("Commands:")
    print("  help - Display this help message")
    print("  login <url> - Log in to the system")
    print("  logout - Log out of the system")
    print("  post - Post a new story")
    print("  list - List all news sites")
    print("  news - Get the lastest news")
    print("     [Options]")
    print("       [-id=] - id of the news service")
    print("       [-cat=] - category of news")
    print("       [-reg=] - region of news")
    print("       [-date=] - date of news")
    print("  exit - Exit the program")

def main():
    session_url = ""
    input_prompt = ">> "
    session = requests.Session()
    
    while True:
        print(input_prompt, end="")

        # Get user input
        user_input = input()

        input_list = user_input.split(" ")

        if input_list[0] == "exit":
            break
        
        if input_list[0] == "login":
            print(input_prompt + "username: ", end="")
            username = input()
            print(input_prompt + "password: ", end="")
            password = input()

            session_url = login(session, input_list[1], username, password)

        if input_list[0] == "logout":
            if session_url != "":
                logout(session, session_url)
                session_url = ""
            else:
                print("Not logged in")

        if input_list[0] == "post":
            if session_url == "":
                print("Not logged in")
            else:
                print(input_prompt + "headline: ", end="")
                headline = input()
                print(input_prompt + "category (pol, art, tech, trivia): ", end="")
                category = input()
                print(input_prompt + "region (uk, eu, w): ", end="")
                region = input()
                print(input_prompt + "details: ", end="")
                details = input()
    
                post(session, session_url, headline, category, region, details)

        if input_list[0] == "news":
            options = parse_news_options(input_list[1:])

            news(options)

        if input_list[0] == "list":
            list_news_sites()

        if input_list[0] == "delete":
            if session_url != "":
                delete(session, session_url, input_list[1])
            else:
                print("not logged in")

        if input_list[0] == "help":
            display_help()

main()