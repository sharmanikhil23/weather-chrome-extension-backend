from django.http import HttpResponse, JsonResponse
import requests
import environ
env = environ.Env()
environ.Env.read_env()

# Create your views here.
def getWeather(request):

    try:
        latitide=request.GET.get('latitude')
        longitude=request.GET.get('longitude')

        url = f'http://api.weatherapi.com/v1/forecast.json?key={env('WEATHER_API_KEY')}&q={latitide},{longitude}&days=4&aqi=yes&alerts=yes';
        
        response=requests.get(url)
        if (response.status_code==200):
            data=response.json()
            return JsonResponse(data)
        elif (response.status_code==400):
            print("location error from weather API");
            return JsonResponse({'status': 400, 'message': 'Incorrect location'}, status=400)
        elif (response.status_code==401):
            print("API key error from weather api")
            return JsonResponse({'status': 401, 'message': 'developer server error'}, status=401)
        elif (response.status_code==500):
            print("Weather Server provider Error")
            return JsonResponse({'status': 500, 'message': 'provider server error'}, status=500)
       
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return JsonResponse({'status': 422, 'message': 'Request error occurred'}, status=422)
    
    except Exception as e:
        print("Unexpected error:", e)
        return JsonResponse({'status': 422, 'message': 'Unexpected error occurred'}, status=422)