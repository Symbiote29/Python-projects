from datetime import datetime

def save_to_file(url, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("search_results.txt", "a", encoding="utf-8") as file:
        file.write(f"Date: {timestamp}\n")
        file.write(f"URL: {url}\n")
        file.write(f"Data: {data}\n\n")

def read_from_file():
    with open("search_results.txt", "r", encoding="utf-8") as file:
        print(file.read())