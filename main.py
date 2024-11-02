from notion_client import Client
from datetime import datetime, timedelta


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

def retrieve_title(data):
    """
    Retrieve the titles from the data.

    Args:
    data (list): A list of dictionaries where each dictionary represents a page.

    Returns:
    None
    """
    result = []
    # Iterate over each item in the data
    for i, _ in enumerate(data):
        # Retrieve the title from the page properties
        title = data[i]['properties']['Name']['title'][0]['plain_text']
        # Print the title
        result.append(title)
    return result

def create_page(notion, database_id, page_title, due_date):
    new_page = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": page_title
                    }
                }
            ]},
        "Deadline": {
            "date": {
                "start": due_date.isoformat(),  # Format the date as an ISO 8601 string
                "end": None,  # Set to None if you don't have an end date
                "time_zone": None  # You can specify a time zone if needed
            }
        },
    }

    try:
        # Create the new page in the database
        response = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=new_page
        )
        # Print success message
        print("Page created successfully!")

    except Exception as e:
        # Print any errors that occur
        print("An error occurred while creating the page:", e)

def times_occurence(kind, times, title, date):
    for i in range(times):
        match kind:
            case "daily":
                create_page(notion, DATABASE_ID, title, date)
                date+= timedelta(days=1)
            case "weekly":
                create_page(notion, DATABASE_ID, title, date)
                date+= timedelta(weeks=1)
            case "monthly":
                create_page(notion, DATABASE_ID, title, date)
                date+=timedelta(weeks=4)
def till_date(kind, title, deadline):
    date = datetime.today()
    while date<=deadline:
        match kind:
            case "daily":
                create_page(notion, DATABASE_ID, title, date)
                date+=timedelta(days=1)
            case "weekly":
                create_page(notion, DATABASE_ID, title, date)
                date+= timedelta(weeks=1)
            case "monthly":
                create_page(notion, DATABASE_ID, title, date)
                date+=timedelta(weeks=4)


def main():
    global notion
    notion = Client(auth=NOTION_API_KEY)
    
    till_date("weekly", "Hello World", datetime(2024, 11, 10))




if __name__ == "__main__":
    main()
