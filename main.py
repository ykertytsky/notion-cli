# Init 
# Reading DB 

import os 
from notion_client import Client
from datetime import datetime, timedelta
from pprint import pprint

import json

from config import NOTION_API_KEY, DATABASE_ID





def write_to_json(data, filename):
    """
    Write data to a JSON file.
    
    Args:
    data (dict): The data to write to the file.
    filename (str): The name of the file to write to.
    """
    # Open the file in write mode
    with open(filename, "w", encoding="utf-8") as f:
        # Dump the data to the file in JSON format
        json.dump(data, f, ensure_ascii=False)

def main():
    notion = Client(auth=NOTION_API_KEY)

    data = notion.databases.query(DATABASE_ID)['results']

    for i, _ in enumerate(data):
        title = data[i]['properties']['Name']['title'][0]['plain_text']
        pprint(title)

    write_to_json(data, "output.json")


if __name__ == "__main__":
    main()
