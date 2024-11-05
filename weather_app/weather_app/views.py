from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import requests


def home(request):
    location=request.GET.get('location')
    
    try:
        coordinates_url =  request.build_absolute_uri('/geolocation/' + f'?location={location}')
        response = requests.get(coordinates_url)
        print(response)
        if(response.status_code==200):
            data=response.json()
            weather_url=request.build_absolute_uri('/weather/' + f'?latitude={data["latitude"]}&longitude={data["longitude"]}')
            response = requests.get(weather_url)
            data=response.json()
            return JsonResponse(data)
        else:
            return JsonResponse(response.json())
    except Exception as e:
        print(f'{e}')

def main(request):
    return HttpResponse("Your server is working")