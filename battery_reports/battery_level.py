from common_utilities.smartthings import SmartThingsClient
import os
import traceback
import json
from common_utilities import setuplogger
from battery_reports import html_generator
from common_utilities.sesactions import SesActions

logger = None


def lambda_handler(event, context):
    try:
        process(True)
    except:
        print(traceback.format_exc())


def process(lambda_invocation):
    logger = setuplogger.create_logger(__name__, 'INFO', not lambda_invocation)

    parameters = get_parameters()
    smart_things_client = parameters[0]
    battery_low_level_threshold = parameters[1]
    from_address = parameters[2]
    to_addresses = [parameters[3]]
    ses_client = SesActions()

    locations = smart_things_client.get_locations()
    logger.debug('Locations: ' + json.dumps(locations))
    battery_enabled_devices = smart_things_client.get_devices_with_capabilities('battery')
    battery_level_devices = get_battery_level(smart_things_client, battery_enabled_devices)
    logger.debug('Devices: ' + json.dumps(battery_level_devices))
    sort_by_battery_level(battery_level_devices)
    logger.debug('Devices Sorted by Battery Level: ' + json.dumps(battery_level_devices))
    html_report = html_generator.create_email_body(battery_level_devices, locations, {'%': battery_low_level_threshold})
    logger.debug(html_report)
    ses_client.send_email(from_address, to_addresses, 'SmartThings Battery Level Report', html_report, 'Html')
    logger.info('Battery Level Report sent.')


def get_parameters():
    smart_things_client = SmartThingsClient(os.environ['AUTHZ_TOKEN'])
    battery_low_level_threshold = int(os.environ['MIN_ACCEPTABLE_BATTERY_LEVEL']) if 'MIN_ACCEPTABLE_BATTERY_LEVEL' in \
                                                                               os.environ else 10
    from_address = os.environ['FROM_ADDRESS']
    to_address = os.environ['TO_ADDRESS']
    return smart_things_client, battery_low_level_threshold, from_address, to_address


def get_battery_level(smart_things_client, devices):
    battery_level_devices = {}
    for device in devices:
        device_status = smart_things_client.get_device_status(device[0]['deviceId'])
        battery_level = device_status['components'][device[1][0]]['battery']['battery']
        if 'unit' not in battery_level:
            battery_level['unit'] = '%'
        if battery_level['unit'] not in battery_level_devices:
            battery_level_devices[battery_level['unit']] = []
        device[0]['battery_value'] = battery_level['value']
        battery_level_devices[battery_level['unit']].append(device[0])
    return battery_level_devices


def sort_by_battery_level(devices):
    for unit_type in devices:
        devices[unit_type].sort(key=lambda x: x['battery_value'])
