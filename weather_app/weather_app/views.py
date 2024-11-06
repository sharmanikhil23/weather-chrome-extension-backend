import httpx
from django.http import JsonResponse, HttpResponse

# Make the home view asynchronous
async def home(request):
    location = request.GET.get('location')
    if not location:
        return JsonResponse({'message': "Location parameter is required", 'status': 400}, status=400)

    # Use the async httpx client to make requests
    async with httpx.AsyncClient() as client:
        try:
            # Build the geolocation URL
            coordinates_url = request.build_absolute_uri(f'/geolocation/?location={location}')
            
            # Make the asynchronous GET request to the geolocation service
            coordinates_response = await client.get(coordinates_url, timeout=10)
            
            if coordinates_response.status_code == 200:
                data = coordinates_response.json()  # Get the JSON data from the response
                
                # Build the weather URL using the geolocation data
                weather_url = request.build_absolute_uri(f'/weather/?latitude={data["latitude"]}&longitude={data["longitude"]}')
                
                # Make the asynchronous GET request to the weather service
                weather_response = await client.get(weather_url, timeout=10)
                
                if weather_response.status_code == 200:
                    return JsonResponse(weather_response.json())  # Return weather data as JSON response
                else:
                    return JsonResponse(weather_response.json(), status=weather_response.status_code)
            else:
                return JsonResponse(coordinates_response.json(), status=coordinates_response.status_code)

        except httpx.TimeoutException:
            return JsonResponse({'message': 'Request timed out', 'status': 408}, status=408)
        except httpx.RequestError as e:
            # Catch other HTTP-related errors
            return JsonResponse({'message': str(e), 'status': 500}, status=500)
        except Exception as e:
            # General exception handling for any other unexpected errors
            return JsonResponse({'message': str(e), 'status': 500}, status=500)

# Optional: Main health check view
def main(request):
    return HttpResponse("Your server is working")
