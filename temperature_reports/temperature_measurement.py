from common_utilities.smartthings import SmartThingsClient
import os
import json
from common_utilities import setuplogger
from temperature_reports import html_generator
from common_utilities.sesactions import SesActions

logger = None


def lambda_handler(event, context):
    process(True)


def process(lambda_invocation):
    logger = setuplogger.create_logger(__name__, 'DEBUG', not lambda_invocation)

    parameters = get_parameters()
    smart_things_client = SmartThingsClient(parameters['AUTHZ_TOKEN'])
    ses_client = SesActions()

    locations = smart_things_client.get_locations()
    logger.debug('Locations: ' + json.dumps(locations))
    temperature_enabled_devices = smart_things_client.get_devices_with_capabilities('temperatureMeasurement')
    temperature_values = get_temperature_values(smart_things_client, temperature_enabled_devices, parameters['TEMPERATURE_UNIT'])
    logger.debug('Devices: ' + json.dumps(temperature_values))
    sort_by_temperature_level(temperature_values)
    logger.debug('Devices Sorted by Temperature Level: ' + json.dumps(temperature_values))
    html_report = html_generator.create_email_body(temperature_values, locations, parameters['LOW_TEMPERATURE_LIMIT'],
                                                   parameters['HIGH_TEMPERATURE_LIMIT'])
    logger.debug(html_report)
    ses_client.send_email(parameters['FROM_ADDRESS'], parameters['TO_ADDRESS'], 'SmartThings Temperature Level Report', html_report, 'Html')
    logger.info('Temperature Level Report sent.')


def get_parameters():
    authz_token = os.environ['AUTHZ_TOKEN']
    temperature_unit = os.environ['TEMPERATURE_UNIT'] if 'TEMPERATURE_UNIT' in os.environ else None
    high_temp_limit = int(os.environ['HIGH_TEMPERATURE_LIMIT'])
    low_temp_limit = int(os.environ['LOW_TEMPERATURE_LIMIT'])
    from_address = os.environ['FROM_ADDRESS']
    to_address = [os.environ['TO_ADDRESS']]
    return {'AUTHZ_TOKEN': authz_token, 'TEMPERATURE_UNIT': temperature_unit,
            'HIGH_TEMPERATURE_LIMIT': high_temp_limit, 'LOW_TEMPERATURE_LIMIT': low_temp_limit,
            'FROM_ADDRESS': from_address, 'TO_ADDRESS': to_address}


def get_temperature_values(smart_things_client, devices, temperature_unit):
    temperature_devices = {}
    for temp_device in devices:
        device = temp_device[0]
        component = temp_device[1]
        device_status = smart_things_client.get_device_status(device['deviceId'])
        temperature = device_status['components'][component[0]]['temperatureMeasurement']['temperature']
        if 'unit' not in temperature:
            temperature['unit'] = 'F'
        converted_temperature = convert_temperature_value(temperature['value'], temperature['unit'], temperature_unit)
        device['temperature_value'] = converted_temperature[0]
        temp_unit = converted_temperature[1]
        device['temperature_unit'] = temp_unit
        if temp_unit not in temperature_devices:
            temperature_devices[temp_unit] = []
        temperature_devices[temp_unit].append(device)

    return temperature_devices


def convert_temperature_value(value, desired_unit, actual_unit):
    if desired_unit == actual_unit:
        return value, desired_unit

    if desired_unit == 'F' and actual_unit == 'C':
        return 9.0/5.0 * value + 32, 'F'

    if desired_unit == 'C' and actual_unit == 'F':
        return (value - 32) * 5.0/9.0, 'C'

    return value, actual_unit




def sort_by_temperature_level(devices):
    for unit_type in devices:
        devices[unit_type].sort(key=lambda x: x['temperature_value'])
