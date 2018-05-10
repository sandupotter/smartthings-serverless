import requests

SMART_THINGS_API_BASE_URL = 'https://api.smartthings.com/v1/'
SMART_THINGS_DEVICES_URL = SMART_THINGS_API_BASE_URL + 'devices'
SMART_THINGS_LOCATIONS_URL = SMART_THINGS_API_BASE_URL + 'locations'
SMART_THINGS_DEVICE_STATUS_URL = SMART_THINGS_API_BASE_URL + 'devices/%s/status'

MAX_ROWS_PER_GET = 50


class SmartThingsClient:

    def __init__(self, auth_token):
        self.authz_header = {'Authorization': 'Bearer ' + auth_token}

    r"""Get all devices that match all requested capabilities.

    :param requested_capabilities: A single capability (as string) or a list of capabilities to match.
    :return: Matching devices
    :rtype: A list of touples: [(device dict, list of component ids that matched all the requested capabilities)]
    """

    def get_devices_with_capabilities(self, requested_capabilities):

        if not isinstance(requested_capabilities, list):
            requested_capabilities = [requested_capabilities]

        all_devices = self.get_all_devices()
        result = []

        for device in all_devices:
            components_with_requested_capabilities = []
            for component in device['components']:
                has_all_capabilities = True
                component_capabilities = []
                for component_capability in component['capabilities']:
                    component_capabilities.append(component_capability['id'])
                for requested_capability in requested_capabilities:
                    if requested_capability not in component_capabilities:
                        has_all_capabilities = False
                if has_all_capabilities:
                    components_with_requested_capabilities.append(component['id'])
            if len(components_with_requested_capabilities) > 0:
                result.append((device, components_with_requested_capabilities))
        return result

    def get_all_devices(self, devices=None, next_url=None):
        devices_url = next_url if next_url is not None else SMART_THINGS_DEVICES_URL + '?rows=%s' % MAX_ROWS_PER_GET
        devices_response = requests.get(devices_url, headers=self.authz_header).json()

        if devices is None:
            devices = devices_response['items']
        else:
            devices += devices_response['items']
        if '_links' in devices_response and 'next' in devices_response['_links'] and \
                devices_response['_links']['next'] is not None:
            return self.get_all_devices(devices, devices_response['_links']['next']['href'])
        else:
            return devices

    def get_locations(self):
        locations_raw = self.get_st_result(SMART_THINGS_LOCATIONS_URL)['items']
        locations = {}
        for location_raw in locations_raw:
            locations[location_raw['locationId']] = location_raw['name']
        return locations

    def get_device_status(self, device_id):
        return self.get_st_result(SMART_THINGS_DEVICE_STATUS_URL % device_id)

    def get_st_result(self, url):
        r = requests.get(url, headers=self.authz_header)
        if r.status_code > 201:
            raise Exception('SmartThings API Code failed. Http status code: %s. Reason: %s.' % (str(r.status_code),
                             r.reason))
        return r.json()
