import os

os.environ["GOOGLE_SUBJECT"] = ""
os.environ["FHEM_IP"] = ""
os.environ["FHEM_VITOCONNECT_OBJECT"] = ""
os.environ["EARLY_DUTY_LABEL"] = "Anja Frühdienst"
os.environ["LATE_DUTY_LABEL"] = "Anja Spätdienst"
os.environ["NIGHT_DUTY_LABEL"] = "Anja Nachtdienst"

import calendar_pump
import datetime
import json
import unittest


class MyTestCase(unittest.TestCase):

    events = []

    def setUp(self) -> None:
        with open('resources/events', 'r') as f_testfile:
            self.events = json.load(f_testfile)

    def test_thursday_early(self):
        utc_now = datetime.datetime(2022, 3, 26, 0, 0, 0, 0)
        utc_end = utc_now + datetime.timedelta(days=7)
        result = calendar_pump.calc_times(self.events, utc_end, utc_now)
        print(result)
        self.assertEqual(result, {'sat': [{'start': '08:00', 'position': 0, 'end': '09:30', 'mode': '5/25-cycles'}, {'start': '11:40', 'position': 1, 'end': '19:30', 'mode': '5/25-cycles'}], 'sun': [{'start': '08:00', 'position': 0, 'end': '09:30', 'mode': '5/25-cycles'}, {'start': '11:40', 'position': 1, 'end': '19:30', 'mode': '5/25-cycles'}], 'mon': [{'start': '05:50', 'position': 0, 'end': '06:30', 'mode': '5/25-cycles'}, {'start': '11:40', 'position': 1, 'end': '19:30', 'mode': '5/25-cycles'}], 'tue': [{'start': '05:50', 'position': 0, 'end': '06:30', 'mode': '5/25-cycles'}, {'start': '09:00', 'position': 1, 'end': '13:00', 'mode': '5/25-cycles'}, {'start': '16:30', 'position': 2, 'end': '19:30', 'mode': '5/25-cycles'}], 'wed': [{'start': '05:50', 'position': 0, 'end': '06:30', 'mode': '5/25-cycles'}, {'start': '09:00', 'position': 1, 'end': '13:00', 'mode': '5/25-cycles'}, {'start': '16:30', 'position': 2, 'end': '19:30', 'mode': '5/25-cycles'}], 'thu': [{'start': '04:00', 'position': 0, 'end': '06:30', 'mode': '5/25-cycles'}, {'start': '11:45', 'position': 1, 'end': '19:30', 'mode': '5/25-cycles'}], 'fri': [{'start': '05:50', 'position': 0, 'end': '06:30', 'mode': '5/25-cycles'}, {'start': '09:00', 'position': 1, 'end': '13:00', 'mode': '5/25-cycles'}, {'start': '16:30', 'position': 2, 'end': '19:30', 'mode': '5/25-cycles'}]})


if __name__ == '__main__':
    unittest.main()
