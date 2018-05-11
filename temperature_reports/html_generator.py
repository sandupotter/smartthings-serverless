from jinja2 import Environment, PackageLoader, select_autoescape


def create_email_body(devices, locations, temperature_low_limit, temperature_high_limit):
    env = Environment(
        loader=PackageLoader('temperature_reports', 'templates'),
        autoescape=select_autoescape(['html']),
        trim_blocks=True
    )
    template_table = env.get_template('temperature_level_table.html')
    device_tables = []
    for device_data in get_devices_data(devices, locations, temperature_low_limit, temperature_high_limit):
        device_table_html = template_table.render(devices_low_temperature_level=device_data[0],
                                                  devices_high_temperature_level=device_data[1],
                                                  devices_acceptable_temperature_level=device_data[2],
                                                  temperature_low_limit=device_data[3],
                                                  temperature_high_limit=device_data[4],
                                                  temperature_unit=device_data[5])
        device_tables.append(device_table_html)
    template = env.get_template('temperature_level.html')
    return template.render(device_tables=device_tables)


def get_devices_data(devices, locations, temperature_low_limit, temperature_high_limit):
    devices_data = []
    for temperature_unit in devices:
        devices_low_temperature_level = []
        devices_high_temperature_level = []
        devices_acceptable_temperature_level = []
        for device in devices[temperature_unit]:
            device_data = {'name': device['label'], 'type': device['deviceTypeName'],
                           'location': locations[device['locationId']],
                           'temperature_value': device['temperature_value']}
            if device_data['temperature_value'] <= temperature_low_limit:
                devices_low_temperature_level.append(device_data)
            elif device_data['temperature_value'] >= temperature_high_limit:
                devices_high_temperature_level.append(device_data)
            else:
                devices_acceptable_temperature_level.append(device_data)
        devices_data.append((devices_low_temperature_level, devices_high_temperature_level,
                             devices_acceptable_temperature_level, temperature_low_limit,
                             temperature_high_limit, temperature_unit))
    return devices_data
