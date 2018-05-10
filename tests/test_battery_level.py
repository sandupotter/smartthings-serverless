import unittest
from battery_reports import battery_level


class BatteryReports(unittest.TestCase):


    def test_battery_level(self):
        battery_level.process(False)


if __name__ == '__main__':
    unittest.main()
