import unittest
import os
from common_utilities.smartthings import SmartThingsClient


class SmartThingsHelpers(unittest.TestCase):

    smart_things_client = SmartThingsClient(os.environ['AUTHZ_TOKEN'])

    def test_get_devices_with_capabilites(self):
        devices = self.smart_things_client.get_devices_with_capabilities('battery')
        self.assertGreater(len(devices),0)


if __name__ == '__main__':
    unittest.main()
