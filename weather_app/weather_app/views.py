import asyncio
from django.http import JsonResponse, HttpResponse
from .location import getGeolocation
from .weather import getWeather

# Make the home view asynchronous
async def home(request):
    location = request.GET.get('location')
    if not location:
        return JsonResponse({'message': "Location parameter is required", 'status': 400}, status=400)
    
    location=await getGeolocation(location)
    
    if location.get('status') != 200:
        print("Reached here")
        return JsonResponse(location)
    else:
        latitude = location.get('latitude')
        longitude = location.get('longitude')
        weather=await getWeather(latitude,longitude)
        return JsonResponse(weather)

# Optional: Main health check view
def main(request):
    return HttpResponse("Your server is working")
