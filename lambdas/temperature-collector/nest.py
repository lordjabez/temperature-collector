import logging

import requests


_log = logging.getLogger(__name__)


def _celsius_to_fahrenheit(temperature):
    return temperature * 1.8 + 32.0


def _get_session(config):
    session = requests.Session()
    url = 'https://www.googleapis.com/oauth2/v4/token'
    params = {
        'client_id': config['nestClientId'],
        'client_secret': config['nestClientSecret'],
        'refresh_token': config['nestRefreshToken'],
        'grant_type': 'refresh_token',
    }
    response = requests.post(url, params=params)
    token_data = response.json()
    token_type = token_data['token_type']
    access_token = token_data['access_token']
    auth_header = {'Authorization': f'{token_type} {access_token}'}
    _log.info('Refreshed Nest access token')
    session.headers.update(auth_header)
    return session


def _get_devices(config, session):
    project_id = config['nestProjectId']
    devices_url = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices'
    response = session.get(devices_url)
    _log.info(f'Received Nest response: {response}')
    return response.json()['devices']


def _parse_device(device):
    thermostat = {}
    traits = device['traits']
    if traits['sdm.devices.traits.Connectivity']['status'] == 'ONLINE':
        temperature = traits['sdm.devices.traits.Temperature']['ambientTemperatureCelsius']
        thermostat['temperature'] = _celsius_to_fahrenheit(temperature)
        setpoint = traits['sdm.devices.traits.ThermostatTemperatureSetpoint']
        if 'coolCelsius' in setpoint:
            thermostat['coolsetpoint'] = _celsius_to_fahrenheit(setpoint['coolCelsius'])
        if 'heatCelsius' in setpoint:
            thermostat['heatsetpoint'] = _celsius_to_fahrenheit(setpoint['heatCelsius'])
    return thermostat


def get_thermostats(config):
    session = _get_session(config)
    devices = _get_devices(config, session)
    return {
        'downstairs': _parse_device(devices[0]),
    }
