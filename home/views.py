from django.shortcuts import render
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'home/index.html')


def login(request):
    return render(request, 'home/login.html')


def signup(request):
    return render(request, 'home/signup.html')


def test(request):
    return JsonResponse({
        'data': [
            {'name': 'tag1', 'count': 10, 'image_urls': ['https://scontent.xx.fbcdn.net/hprofile-xfa1/v/t1.0-1/11145072_10152780321362483_2068237063183610202_n.jpg?oh=8184c4abe81df531ff224a6c84c609e0&oe=57AB7E5F','https://scontent.xx.fbcdn.net/hprofile-xfa1/v/t1.0-1/11145072_10152780321362483_2068237063183610202_n.jpg?oh=8184c4abe81df531ff224a6c84c609e0&oe=57AB7E5F','https://scontent.xx.fbcdn.net/hprofile-xfa1/v/t1.0-1/11145072_10152780321362483_2068237063183610202_n.jpg?oh=8184c4abe81df531ff224a6c84c609e0&oe=57AB7E5F']},
            {'name': 'tag2', 'count': 10, 'image_urls': []},
            {'name': 'tag3', 'count': 10, 'image_urls': ['https://scontent.xx.fbcdn.net/hprofile-xfa1/v/t1.0-1/11145072_10152780321362483_2068237063183610202_n.jpg?oh=8184c4abe81df531ff224a6c84c609e0&oe=57AB7E5F']},
            {'name': 'tag4', 'count': 100, 'image_urls': []},
            {'name': 'tag5', 'count': 1, 'image_urls': []},
            {'name': 'tag6', 'count': 12, 'image_urls': ['https://scontent.xx.fbcdn.net/hprofile-xfa1/v/t1.0-1/11145072_10152780321362483_2068237063183610202_n.jpg?oh=8184c4abe81df531ff224a6c84c609e0&oe=57AB7E5F']},
        ]
    })

