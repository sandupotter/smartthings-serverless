from jinja2 import Environment, PackageLoader, select_autoescape


def create_email_body(devices, locations, battery_low_threshold):
    env = Environment(
        #loader=FileSystemLoader('../templates'),
        loader=PackageLoader('battery_reports', 'templates'),
        autoescape=select_autoescape(['html']),
        trim_blocks=True
    )
    template_table = env.get_template('battery_level_table.html')
    device_tables = []
    for device_data in get_devices_data(devices, locations, battery_low_threshold):
        device_table_html = template_table.render(devices_low_battery_level=device_data[0],
                                                  devices_acceptable_battery_level=device_data[1],
                                                  battery_low_threshold=device_data[2], battery_unit=device_data[3])
        device_tables.append(device_table_html)
    template = env.get_template('battery_level.html')
    return template.render(device_tables=device_tables)


def get_devices_data(devices, locations, battery_low_threshold):
    devices_data = []
    for battery_unit in devices:
        devices_low_battery_level = []
        devices_acceptable_battery_level = []
        for device in devices[battery_unit]:
            device_data = {'name': device['label'], 'type': device['deviceTypeName'], 'location': locations[device['locationId']],
                           'battery_value': device['battery_value']}
            if device_data['battery_value'] <= battery_low_threshold[battery_unit]:
                devices_low_battery_level.append(device_data)
            else:
                devices_acceptable_battery_level.append(device_data)
        devices_data.append((devices_low_battery_level, devices_acceptable_battery_level,
                             battery_low_threshold[battery_unit], battery_unit))
    return devices_data
