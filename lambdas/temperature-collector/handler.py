import logging
import os

import configuration
import honeywell
import metrics
import nest
import weather


_debug_logging = os.environ.get('DEBUG_LOGGING') == 'true'
_log_format = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
_log_level = logging.DEBUG if _debug_logging else logging.INFO
root_logger = logging.getLogger()
for handler in root_logger.handlers or []:
    root_logger.removeHandler(handler)
logging.basicConfig(format=_log_format, level=_log_level)

_log = logging.getLogger(__name__)


def _get_lat_lon(position):
    return (float(i) for i in position.split(','))


def _collect_location(config, name, lat, lon, interface):
    try:
        temperature = weather.get_temperature(config, lat, lon)
        thermostats = interface.get_thermostats(config)
        metrics.put(name, temperature, thermostats)
    except Exception as error:
        _log.error(f'An error occurred while collecting {name}: {error}')


def _collect_grey_haven(config):
    lat, lon = _get_lat_lon(config['greyHavenLocation'])
    _collect_location(config, 'TheGreyHaven', lat, lon, honeywell)


def _collect_san_diego(config):
    lat, lon = _get_lat_lon(config['sanDiegoLocation'])
    _collect_location(config, 'SanDiego', lat, lon, nest)


def lambda_handler(event, context):
    config = configuration.get()
    _collect_grey_haven(config)
    _collect_san_diego(config)
