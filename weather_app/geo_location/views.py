from django.shortcuts import render
from django.http import JsonResponse
import requests
import environ

# Initialize the environment variables
env = environ.Env()
environ.Env.read_env()

def getGeolocation(request):
    location = request.GET.get('location')  
    if not location:
        return JsonResponse({'message': "Location parameter is required", 'status': 400}, status=400)

    try:
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={env("MAPBOXKEY")}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if len(data.get('features', [])) == 0:
                return JsonResponse({'message': "Incorrect location provided", 'status': 422}, status=422)
                print("still herer")
            # Extract latitude and longitude
            latitude = data['features'][0]['center'][1]
            longitude = data['features'][0]['center'][0]
            
            # Return as a JSON response
            return JsonResponse({'latitude': latitude, 'longitude': longitude, 'status': 200}, status=200)
        
        elif response.status_code == 401:
            return JsonResponse({'status': 401, 'message': 'Unauthorized access to the provider'}, status=401)
        
        # For other unexpected status codes
        return JsonResponse({'status': response.status_code, 'message': 'Unable to fetch geolocation data'}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return JsonResponse({'status': 422, 'message': 'Request error occurred'}, status=422)
    
    except Exception as e:
        print("Unexpected error:", e)
        return JsonResponse({'status': 500, 'message': 'Unexpected error occurred'}, status=500)

