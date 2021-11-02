import json

with open('bookmarks.json', 'r') as file:
    dict = json.load(file)
    print(json.dumps(dict[276], indent=2))