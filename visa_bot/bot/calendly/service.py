import os

from requests import get, post
from dotenv import load_dotenv

load_dotenv()

CALENDLY_API_KEY = os.environ.get("CALENDLY_API_KEY")


def get_available_slots():
    url = "https://api.calendly.com/scheduled_events"
    headers = {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = get(url, headers=headers)
    return response.json()


def schedule_appointment(user_data):
    url = "https://api.calendly.com/scheduled_events"
    headers = {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        # Your scheduling data here
    }
    response = post(url, headers=headers, json=data)
    return response.json()
