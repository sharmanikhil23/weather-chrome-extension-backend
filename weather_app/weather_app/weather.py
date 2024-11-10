# location.py
import httpx
from django.conf import settings

async def getWeather(latitude,longitude):  
    if not latitude or not longitude:
        return {'message': "Location parameter is required", 'status': 400}

    try:
        url = f'http://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API_KEY}&q={latitude},{longitude}&days=4&aqi=yes&alerts=yes';
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if (response.status_code==200):
            data=response.json()
            data['status']=response.status_code
            return data
        elif (response.status_code==400):
            print("location error from weather API");
            return {'status': 400, 'message': 'Incorrect location'}
        elif (response.status_code==401):
            print("API key error from weather api")
            return {'status': 401, 'message': 'developer server error'}
        elif (response.status_code==500):
            print("Weather Server provider Error")
            return {'status': 500, 'message': 'provider server error'}
       
    except httpx.RequestError as e:
        print("Request error:", e)
        return {'status': 422, 'message': 'Request error occurred'}
    
    except Exception as e:
        print("Unexpected error:", e)
        return {'status': 500, 'message': 'Unexpected error occurred'}



