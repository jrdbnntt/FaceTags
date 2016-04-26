from __future__ import print_function
from clarifai.client import ClarifaiApi
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from models import FacebookImage, Tag
import requests
import random

CLARIFAI_MAX = 128


def index(request):
    return HttpResponse("Hello mah niggah")


def get_user(request):
    token = request.GET["token"]
    try:
        friend_img_urls = pull_friends_from_facebook(token)
        friends, remaining_friend_urls = pull_stored_tags(friend_img_urls)
        if len(remaining_friend_urls) > 0:
            max_new_friends = remaining_friend_urls if CLARIFAI_MAX > remaining_friend_urls else CLARIFAI_MAX
            new_friends = pull_tags_from_clarafai(random.sample(remaining_friend_urls, max_new_friends))
            friends.extend(new_friends)
            store_new_friends(new_friends)

            print('Got {} friends, ({} newly tagged, {} from db)'.format(
                len(friends), len(new_friends), len(friends) - len(new_friends)
            ))
        else:
            print('Got {} friends, all from db'.format(len(friends)))

        return JsonResponse({
            'data': group_tags(friends)
        })

    except ValueError as e:
        print(e)
        return JsonResponse({
            'data': []
        })


def pull_friends_from_facebook(token):
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
            if not person["picture"]["data"]["is_silhouette"] \
                    and person["picture"]["data"]["height"] > 250 \
                    and person["picture"]["data"]["width"] > 250:
                friends.append(person["picture"]["data"]["url"])
        try:
            r = requests.get(r.json()["paging"]["next"], params=params)
        except KeyError:
            break

    return friends


def pull_stored_tags(img_urls):
    found = []
    not_found = []

    for url in img_urls:
        try:
            stored_img = FacebookImage.objects.get(url=url)

            img = {'url': stored_img.url, 'tags': []}
            for tag in stored_img.tags.all():
                img['tags'].append(tag.name)

            found.append(img)

        except ObjectDoesNotExist:
            not_found.append(url)

    return found, not_found


def pull_tags_from_clarafai(img_urls):
    friends = []
    clarifai_api = ClarifaiApi()
    clarifai_results = clarifai_api.tag_image_urls(img_urls)

    for image in clarifai_results['results']:
        friend = {'url': image['url'], 'tags': []}

        for i, tag_name in enumerate(image["result"]["tag"]["classes"]):
            if image["result"]["tag"]["probs"][i] >= 0.9:
                friend['tags'].append(tag_name)

        friends.append(friend)

    return friends


def store_new_friends(friends):
    """ Stores friends & tags from the format [{'url', tags[]}] """
    for f in friends:
        img = FacebookImage(url=f['url'])
        img.save()

        for tag in f['tags']:
            # Save if new
            try:
                stored_tag = Tag.objects.get(name=tag)
            except ObjectDoesNotExist:
                stored_tag = Tag(name=tag)
                stored_tag.save()

            img.tags.add(stored_tag)

        img.save()


def group_tags(friends):
    tags = []

    for f in friends:
        for tag_name in f['tags']:
            matching_tag = None
            for tag in tags:
                if tag['name'] == tag_name:
                    matching_tag = tag
                    tag['count'] += 1
                    tag['image_urls'].append(f['url'])
                    break

            if matching_tag is None:
                tags.append({
                    'name': tag_name,
                    'count': 1,
                    'image_urls': [f['url']]
                })

    return tags


def get_all(request):
    """ Gets all tags in the db with counts of use """
    tags = []

    for tag in Tag.objects.all():
        tag_data = {
            'name': tag.name,
            'count': tag.facebookimage_set.distinct().count()
        }
        
        if tag_data['count'] > 0:
            tags.append(tag_data)

    return JsonResponse({'data': tags})


def get_fix(request):
    """ Repairs any database repetition """

    urls = set()

    for img in FacebookImage.objects.all():
        urls.add(img.url)

    for url in urls:
        images = FacebookImage.objects.filter(url=url)

        if len(images) > 1:
            for i in range(1, len(images)):
                images[i].delete()

    return JsonResponse({'result': 'success'})
