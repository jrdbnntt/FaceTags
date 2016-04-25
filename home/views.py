from django.shortcuts import render
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'home/index.html')


def run(request):
    return render(request, 'home/run.html')
