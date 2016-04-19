from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests
import random
from clarifai.client import ClarifaiApi
import pprint

FRIEND_MAX = 25

def index(request):
    return HttpResponse("Hello mah niggah")

def get_user(request):
    token = "CAACEdEose0cBAJR18VzPsOPTJwTxYB3gKjV2z6s5UZCocCxFrZAMcAnixbZBZBm9g8Jqg0AN6lzUxL7aEyDljQ0Aq88Tl9vjRLxnxT72zGKr49UtUBDBaQt1N29JmBjJZBT21YHKiENz119Ge5Tb6Mn85Lsej8wFkLbKJG9Xvgv67oevdZBr1mhJYnWl0qT0z9QVjM5irO6AZDZD"

    params = {
        "access_token": token,
    }
    user_id = requests.get("https://graph.facebook.com/v2.6/me", params=params).json()["id"]

    friends = []
    params = {
        "access_token": token,
        "fields": "picture.height(1200)"
    }
    r = requests.get("https://graph.facebook.com/v2.6/" + user_id + "/invitable_friends", params=params)
    while True:
        for person in r.json()["data"]:
            if not person["picture"]["data"]["is_silhouette"]\
                    and person["picture"]["data"]["height"] > 250\
                    and person["picture"]["data"]["width"] > 250:
                friends.append(person["picture"]["data"]["url"])
        try:
            r = requests.get(r.json()["paging"]["next"], params=params)
        except KeyError:
            break

    clarifai_api = ClarifaiApi()
    random_friends = random.sample(friends, FRIEND_MAX)
    # print ("Sending to Clarifai")

    clarifai_results = clarifai_api.tag_image_urls(random_friends)
    # pprint.pprint(clarifai_results)


    # Gets the counts of each tag
    tags = []
    for image in clarifai_results["results"]:
        for i, tag_name in enumerate(image["result"]["tag"]["classes"]):
            if image["result"]["tag"]["probs"][i] < 0.9:
                continue

            if not any(tag['name'] == tag_name for tag in tags):
                tags.append({
                    "name": tag_name,
                    "count": 1,
                    "image_urls": [image["url"]]
                })
            else:
                for tag in tags:
                    if tag["name"] == tag_name:
                        tag["count"] += 1
                        tag["image_urls"].append(image["url"])
                        break

    tags = {"data": tags}
    # pprint.pprint(tags)

    return JsonResponse(tags)
