import httpx
from django.http import JsonResponse
from django.conf import settings

# Make the getGeolocation view asynchronous
async def getGeolocation(request):
    location = request.GET.get('location')  
    if not location:
        return JsonResponse({'message': "Location parameter is required", 'status': 400}, status=400)

    try:
        # Prepare the URL with the location and access token
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={settings.MAPBOXKEY}'

        # Use httpx.AsyncClient for making asynchronous HTTP requests
        async with httpx.AsyncClient() as client:
            # Perform the asynchronous GET request to the geolocation API
            response = await client.get(url, timeout=10)

            # Check the response status code and handle accordingly
            if response.status_code == 200:
                data = response.json()

                # Check if there are any features returned from the geolocation API
                if len(data.get('features', [])) == 0:
                    return JsonResponse({'message': "Incorrect location provided", 'status': 422}, status=422)

                # Extract latitude and longitude from the response
                latitude = data['features'][0]['center'][1]
                longitude = data['features'][0]['center'][0]

                # Return the latitude and longitude as a JSON response
                return JsonResponse({'latitude': latitude, 'longitude': longitude, 'status': 200}, status=200)
            
            elif response.status_code == 401:
                return JsonResponse({'status': 401, 'message': 'Unauthorized access to the provider'}, status=401)
            
            # Handle other unexpected status codes
            return JsonResponse({'status': response.status_code, 'message': 'Unable to fetch geolocation data'}, status=response.status_code)

    except httpx.RequestError as e:
        return JsonResponse({'status': 422, 'message': 'Request error occurred'}, status=422)
    
    except Exception as e:
        return JsonResponse({'status': 500, 'message': 'Unexpected error occurred'}, status=500)
