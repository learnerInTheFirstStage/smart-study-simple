from collections import defaultdict


def parse_plan(plan_content):
    """
    Parse the plan content returned by ai, parse it ready to be stored into the database
    """
    # plan_content should be formatted as:
    #     "Day1=learn 2 books&Day2=do 3 practices"
    content_of_days = plan_content.split("&")

    topics_data = defaultdict(None)

    for content_of_day in content_of_days:
        day = content_of_day.split('=')
        day_header = day[0]
        day_task = day[1]
        topics_data[day_header] = day_task
    
    return topics_data

# print(store_plan_to_db("Space=learn 2 books&Aero=do 3 practices"))

def parse_practice(practice_content):
    """
    Parse the content of practice into db
    """
    # data should be formatted as:
    #     "Space Aero=learn 2 books&=do 3 practices"