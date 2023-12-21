import requests
import dotenv
import os
from alumniportal.celery import app
from .emails import send_nsfw_report_to_admins, send_nsfw_report_to_user

dotenv.load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/michellejieli/NSFW_text_classifier"
headers = {"Authorization": os.environ["TEXT_NSFW_TOKEN"]}


@app.task(bind=True)
def text_nsfw_checker(self, text: str, instanceId: str, model_name: str) -> str:
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    result = response.json()
    print(result)
    result = sorted(result[0], key=lambda d: d["score"], reverse=True)
    result = result[0]['label']
    print("-------------------------------------------------------------")
    print("::::::::NSFW TEXT CHECKER::::::::")
    print(f"TEXT: {text}")
    print("\n\n")
    print(f"RESULT: {result}")
    print("\n\n")
    if result == 'NSFW':
        print("NSFW TEXT FOUND")
        print("\n\n")
        print(f"DELETING {model_name} Instance.")
        print(f"INSTANCE ID: {instanceId}")
        if (model_name == "Feed"):
            from feed.models import Feed
            feed = Feed.objects.get(id=instanceId)
            feed.isActive = False
            feed.save()
            send_nsfw_report_to_admins(
                feed.id, feed.user.firstName + " " + feed.user.lastName, feed.user.email)
            send_nsfw_report_to_user(
                feed.id, feed.user.firstName + " " + feed.user.lastName, feed.user.email, feed.createdAt.date())
        print("-------------------------------------------------------------")
        return 'NSFW'
    else:
        print("-------------------------------------------------------------")
        return 'SFW'
