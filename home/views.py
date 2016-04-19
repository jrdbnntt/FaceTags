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
            {'name': 'tag1', 'count': 10, 'image_url': 'sdas'},
            {'name': 'tag2', 'count': 10, 'image_url': 'sdas'},
            {'name': 'tag3', 'count': 10, 'image_url': 'sdas'},
            {'name': 'tag4', 'count': 100, 'image_url': 'sdas'},
            {'name': 'tag5', 'count': 1, 'image_url': 'sdas'},
            {'name': 'tag6', 'count': 12, 'image_url': 'sdas'},
        ]
    })

