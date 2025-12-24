import requests 
from django.shortcuts import render
from datetime import datetime
from .services import WeatherService

def home(request):
    # Get location from the URL (or use Boulder,CO as default)
    lat = request.GET.get('lat', '40.0150')
    lon = request.GET.get('lon', '-105.2705')

    data = WeatherService.get_forecast(lat, lon)
    daily_data = data.get('daily', {})

    forecast_list = []

    for i in range(len(daily_data.get('time', []))):
        temp = daily_data['temperature_2m_max'][i]
        rain = daily_data['precipitation_probability_max'][i]
        
        # Get tomorrow's rain if it exists
        tomorrow_rain = None
        if i + 1 < len(daily_data['time']):
            tomorrow_rain = daily_data['precipitation_probability_max'][i+1]

        status, message = get_lawn_advice(temp, rain, tomorrow_rain)

        date_obj = datetime.strptime(daily_data['time'][i], '%Y-%m-%d')
        forecast_list.append({
            'day_name': date_obj.strftime('%A'),
            'day_num': date_obj.strftime('%d'),
            'month': date_obj.strftime('%b'),
            'temp': temp,
            'rain': rain,
            'status': status,
            'msg': message
        })

    context = {'forecast': forecast_list, 'lat': lat, 'lon': lon}
    return render(request, 'advisor/index.html', context)

def get_lawn_advice(temp, rain, next_day_rain=None):
    # Base Logic
    if rain > 50:
        status = "RED"
        message = "STAY OFF: Heavy rain predicted. Nutrients will wash away."
    elif temp > 90:
        status = "RED"
        message = "STAY OFF: Extreme heat. Grass is stressed; fertilizer may burn it."
    elif 60 <= temp <= 85 and rain < 20:
        status = "GREEN"
        message = "IDEAL: Perfect temperature and low rain for application."
    else:
        status = "YELLOW"
        message = "CAUTION: Conditions are okay, but not perfect."

    # Look-ahead Logic
    if status == "GREEN" and next_day_rain is not None and next_day_rain > 70:
        status = "YELLOW"
        message = "CAUTION: Good today, but heavy rain tomorrow could cause runoff."

    return status, message