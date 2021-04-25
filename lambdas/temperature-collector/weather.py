import logging

import requests


_weather_url = 'https://api.openweathermap.org/data/2.5/weather'

_log = logging.getLogger(__name__)


def get_temperature(config, lat, lon):
    api_key = config['openWeatherApiKey']
    params = {'appid': api_key, 'lat': lat, 'lon': lon, 'units': 'imperial'}
    response = requests.get(_weather_url, params=params)
    if response.status_code == requests.codes.ok:
        _log.info(f'OpenWeather call succeeded for {lat} {lon}: {response}')
        weather = response.json()
        return weather['main']['temp']
    else:
        _log.warning('OpenWeather call failed')
