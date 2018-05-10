import unittest
from battery_reports import html_generator


class BatteryReports(unittest.TestCase):


    def test_html_generator(self):
        html_generator.create_email_body(None, None, None)


if __name__ == '__main__':
    unittest.main()
