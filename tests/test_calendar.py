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
        result, _ = calendar_pump.calc_times(self.events, utc_end, utc_now)
        print(result)
        self.assertEqual(result, {'fri': [{'end': '06:30', 'mode': '5/10-cycles', 'position': 0, 'start': '05:50'}, {'end': '13:00', 'mode': '5/25-cycles', 'position': 1, 'start': '09:00'}, {'end': '19:30', 'mode': '5/10-cycles', 'position': 2, 'start': '17:30'}], 'mon': [{'end': '06:30', 'mode': '5/10-cycles', 'position': 0, 'start': '05:50'}, {'end': '19:30', 'mode': '5/25-cycles', 'position': 1, 'start': '11:40'}], 'sat': [{'end': '09:30', 'mode': '5/10-cycles', 'position': 0, 'start': '08:00'}, {'end': '19:30', 'mode': '5/25-cycles', 'position': 1, 'start': '11:40'}], 'sun': [{'end': '09:30', 'mode': '5/10-cycles', 'position': 0, 'start': '08:00'}, {'end': '19:30', 'mode': '5/25-cycles', 'position': 1, 'start': '11:40'}], 'thu': [{'end': '06:30', 'mode': '5/10-cycles', 'position': 0, 'start': '04:00'}, {'end': '19:30', 'mode': '5/25-cycles', 'position': 1, 'start': '11:45'}], 'tue': [{'end': '06:30', 'mode': '5/10-cycles', 'position': 0, 'start': '05:50'}, {'end': '13:00', 'mode': '5/25-cycles', 'position': 1, 'start': '09:00'}, {'end': '19:30', 'mode': '5/10-cycles', 'position': 2, 'start': '17:30'}], 'wed': [{'end': '06:30', 'mode': '5/10-cycles', 'position': 0, 'start': '05:50'}, {'end': '13:00', 'mode': '5/25-cycles', 'position': 1, 'start': '09:00'}, {'end': '19:30', 'mode': '5/10-cycles', 'position': 2, 'start': '17:30'}]})


if __name__ == '__main__':
    unittest.main()
