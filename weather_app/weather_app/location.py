import httpx
from django.conf import settings

async def getGeolocation(location):  
    if not location:
        return {'message': "Location parameter is required", 'status': 400}

    try:
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={settings.MAPBOXKEY}'
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

       
        if response.status_code == 200:
            data = response.json()
            
            if len(data.get('features', [])) == 0:
                return {'message': "Incorrect location provided", 'status': 422}
            
            # Extract latitude and longitude
            latitude = data['features'][0]['center'][1]
            longitude = data['features'][0]['center'][0]
            # Return as a JSON response
            return {'latitude': latitude, 'longitude': longitude, 'status': 200}
        
        elif response.status_code == 401:
            return {'status': 401, 'message': 'Unauthorized access to the provider'}
        
        # For other unexpected status codes
        return {'status': response.status_code, 'message': 'Unable to fetch geolocation data'}

    except httpx.RequestError as e:
        print("Request error:", e)
        return {'status': 422, 'message': 'Request error occurred'}
    
    except Exception as e:
        print("Unexpected error:", e)
        return {'status': 500, 'message': 'Unexpected error occurred'}
