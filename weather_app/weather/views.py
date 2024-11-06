import httpx
from django.http import JsonResponse
from django.conf import settings

# Make the getWeather view asynchronous
async def getWeather(request):

    try:
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if not latitude or not longitude:
            return JsonResponse({'status': 400, 'message': 'Latitude and Longitude are required'}, status=400)

        url = f'http://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API_KEY}&q={latitude},{longitude}&days=4&aqi=yes&alerts=yes'

        async with httpx.AsyncClient() as client:
            # Perform the asynchronous GET request to the weather API
            response = await client.get(url, timeout=10)

            # Check the status code and return the appropriate response
            if response.status_code == 200:
                data = response.json()
                return JsonResponse(data)
            elif response.status_code == 400:
                print("Location error from weather API")
                return JsonResponse({'status': 400, 'message': 'Incorrect location'}, status=400)
            elif response.status_code == 401:
                print("API key error from weather API")
                return JsonResponse({'status': 401, 'message': 'Developer server error'}, status=401)
            elif response.status_code == 500:
                print("Weather provider server error")
                return JsonResponse({'status': 500, 'message': 'Provider server error'}, status=500)

    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return JsonResponse({'status': 422, 'message': 'Request error occurred'}, status=422)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({'status': 422, 'message': 'Unexpected error occurred'}, status=422)
