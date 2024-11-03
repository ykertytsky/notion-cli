"""
Notion CLI by Kertytsky
"""

from datetime import datetime, timedelta


from notion_client import Client
import click




from config import NOTION_API_KEY, DATABASE_ID

notion = Client(auth=NOTION_API_KEY)


@click.group()
def notion_cli():
    pass

@notion_cli.command()
@click.option("--title", 
                        prompt="Title of Your task",
                        help="The Title of Your Task")
@click.option("--due",  
                        default=datetime.today().isoformat()[:10],
                        prompt="Deadline of Your Task (YYYY-MM-DD)",
                        help="The deadline for your task, today by default")
@click.option("--status",
                        default="Not started",
                        prompt="Set the status for your task. ",
                        help="The deadline for your tas, today by default"
              )
def create_task(title, due, status):

    new_page = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]},
        "Deadline": {
            "date": {
                "start": due,
                "end": None, 
                "time_zone": None 
            }
        },
        "Status": {
            "id": "Z%3ClH",
            "type": "status",
            "status": {
                "name": status,
            }}
    }

    try:
        # Create the new page in the database
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=new_page
        )
        # Print success message
        print("Task created successfully!")

    except Exception as e:
        # Print any errors that occur
        print("An error occurred while creating the page:", e)

def times_occurence(notion, kind, times, title, date):
    for _ in range(times):
        match kind:
            case "daily":
                create_task(title, date)
                date+= timedelta(days=1)
            case "weekly":
                create_task(title, date)
                date+= timedelta(weeks=1)
            case "monthly":
                create_task(title, date)
                date+=timedelta(weeks=4)
def till_date(notion, kind, title, deadline):
    date = datetime.today()
    while date<=deadline:
        match kind:
            case "daily":
                create_task(title, date)
                date+=timedelta(days=1)
            case "weekly":
                create_task(title, date)
                date+= timedelta(weeks=1)
            case "monthly":
                create_task(title, date)
                date+=timedelta(weeks=4)


# @click.command()
# @click.option("--title", prompt="Title of Your task",help="The Title of Your Task")
# @click.option("--due", default=datetime.today(), prompt="Deadline of your Task", help="The deadline for your task. Today by default")
# def create_task(notion, title, due):
#     try:
#         create_task(notion=notion, title=title, due=due_date)
#     except Exception as e:
#         print(f'Ooops, {e} happened')



if __name__ == "__main__":
    notion_cli()
