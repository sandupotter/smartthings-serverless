import unittest
from common_utilities.sesactions import SesActions


class EmailActions(unittest.TestCase):
    def test_get_devices_with_capabilites(self):
        SesActions().send_email('sandupotter@gmail.com', ['sandupotter@gmail.com'], 'Test', 'Test')


if __name__ == '__main__':
    unittest.main()
