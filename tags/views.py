from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests
import random
from clarifai.client import ClarifaiApi
import pprint


def index(request):
    return HttpResponse("Hello mah niggah")

def get_user(request, user_id):
    token = "CAACEdEose0cBAEfoBCrnN1ZChlypF1wVvuO6qRPQyBsRCtOA80GLjKeGGl3H2BbebN1OmhD6fdYCEw3IluM7z2cwZADfrT27tFxMIhDNH3buZBBXRBIvLZCl9FqtSdqxoBiutIdXN0qbEYIKWXpFmNrbyF2dwBNR4tC5NxxeKK3flwvUjKOZAIfsxw2RHiEbgxOvR0DGI9gZDZD"

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
    random_friends = random.sample(friends, 2)
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
    pprint.pprint(tags)

    return JsonResponse(tags)
