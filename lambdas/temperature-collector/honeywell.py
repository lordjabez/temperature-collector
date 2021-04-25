import logging

import requests


_base_url = 'https://mytotalconnectcomfort.com/portal'
_headers = {'Content-Type': 'application/json; charset=utf-8', 'X-Requested-With': 'XMLHttpRequest'}

_max_retries = 3

_log = logging.getLogger(__name__)


def _refresh_session(config, session):
    username = config['honeywellUsername']
    password = config['honeywellPassword']
    login_data = {'UserName': username, 'Password': password, 'RememberMe': 'false', 'timeOffset': 480}
    response = session.post(_base_url, data=login_data)
    _log.info(f'Refreshed Honeywell session: {response}')
    return session


def _execute_call(config, session, url, params={}):
    for r in range(_max_retries):
        response = session.post(url, headers=_headers, params=params)
        if response.status_code == requests.codes.ok:
            _log.info(f'Honeywell call succeeded: {response}')
            return response.json()
        else:
            _log.info(f'Honeywell call failed: {response}')
            _refresh_session(config, session)
    _log.warning('Failed to execute Honeywell call')


def _get_device_ids(config, session):
    devices_url = f'{_base_url}/Device/GetZoneListData'
    params = {'locationId': config['honeywellLocationId'], 'page': 1}
    devices = _execute_call(config, session, devices_url, params)
    return [d['DeviceID'] for d in devices]


def _get_device(config, session, device_id):
    device_url = f'{_base_url}/Device/CheckDataSession/{device_id}'
    return _execute_call(config, session, device_url)


def _parse_device(device):
    thermostat = {}
    if device['deviceLive']:
        ui_data = device['latestData']['uiData']
        thermostat['temperature'] = ui_data['DispTemperature']
        if ui_data['SystemSwitchPosition'] in (0, 1, 4):
            thermostat['heatsetpoint'] = ui_data['HeatSetpoint']
        elif ui_data['SystemSwitchPosition'] in (3, 5):
            thermostat['coolsetpoint'] = ui_data['CoolSetpoint']
    return thermostat


def get_thermostats(config):
    session = requests.Session()
    label_parts = (p.split(':') for p in config['honeywellLabels'].split(','))
    labels = {int(p[0]): p[1] for p in label_parts}
    device_ids = _get_device_ids(config, session)
    device_data = {labels[d]: _get_device(config, session, d) for d in device_ids}
    return {
        'downstairs': _parse_device(device_data['downstairs']),
        'upstairs': _parse_device(device_data['upstairs']),
    }
