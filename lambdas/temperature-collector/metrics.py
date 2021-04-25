import datetime
import functools
import logging

import boto3


_log = logging.getLogger(__name__)


def _append_metric(metric_data, timestamp, name, location, value):
    dimensions = [{'Name': 'Location', 'Value': location}]
    metric = {'MetricName': name, 'Dimensions': dimensions, 'Timestamp': timestamp, 'Value': value}
    metric_data.append(metric)


def put(location_name, outside_temperature, thermostat_data):
    downstairs_thermostat = thermostat_data.get('downstairs')
    upstairs_thermostat = thermostat_data.get('upstairs')
    timestamp = datetime.datetime.now()
    namespace = f'Temperatures/{location_name}'
    metric_data = []
    params = {'Namespace': namespace, 'MetricData': metric_data}
    append_metric = functools.partial(_append_metric, metric_data, timestamp)
    if outside_temperature is not None:
        append_metric('Temperature', 'Outside', outside_temperature)
    if downstairs_thermostat:
        append_metric('Temperature', 'Downstairs', downstairs_thermostat['temperature'])
        if 'heatsetpoint' in downstairs_thermostat:
            append_metric('HeatSetpoint', 'Downstairs', downstairs_thermostat['heatsetpoint'])
        if 'coolsetpoint' in downstairs_thermostat:
            append_metric('CoolSetpoint', 'Downstairs', downstairs_thermostat['coolsetpoint'])
    if upstairs_thermostat:
        append_metric('Temperature', 'Upstairs', upstairs_thermostat['temperature'])
        if 'heatsetpoint' in downstairs_thermostat:
            append_metric('HeatSetpoint', 'Upstairs', upstairs_thermostat['heatsetpoint'])
        if 'coolsetpoint' in downstairs_thermostat:
            append_metric('CoolSetpoint', 'Upstairs', upstairs_thermostat['coolsetpoint'])
    _log.info(f'Metric parameters: {params}')
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(**params)
