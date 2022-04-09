import datetime
import fhem
import json
import pathlib
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# If modifying these scopes, delete the file service_account.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SUBJECT = os.environ["GOOGLE_SUBJECT"]
FHEM_IP = os.environ["FHEM_IP"]
FHEM_VITOCONNECT_OBJECT = os.environ["FHEM_VITOCONNECT_OBJECT"]
EARLY_DUTY_LABEL = os.environ["EARLY_DUTY_LABEL"]
LATE_DUTY_LABEL = os.environ["LATE_DUTY_LABEL"]
NIGHT_DUTY_LABEL = os.environ["NIGHT_DUTY_LABEL"]


def main():
    credentials = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    try:
        service = build('calendar', 'v3', credentials=credentials)

        # Call the Calendar API
        utc_now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        now = utc_now.isoformat() + 'Z'  # 'Z' indicates UTC time
        utc_end = (utc_now + datetime.timedelta(days=7))
        events_result = service.events().list(calendarId=SUBJECT, timeMin=now,
                                              timeMax=utc_end.isoformat() + 'Z', singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        result = calc_times(events, utc_end, utc_now)

        print("Sending new schedule to FHEM ...")

        fh = fhem.Fhem(FHEM_IP, protocol="http", port=8083)
        fh.send_cmd(f"""set {FHEM_VITOCONNECT_OBJECT} WW-Zirkulationspumpe_Zeitplan {json.dumps(result)}""")

        print("Done")
    except HttpError as error:
        print('An error occurred: %s' % error)


def calc_times(events, utc_end, utc_now):
    early_duties = []
    late_duties = []
    night_duties = []

    # valid cycles: 5/25 and 5/10
    template_single_entry = """{{"start":"{start}","position":{position},"end":"{end}","mode":"5/{cycle}-cycles"}}"""
    early_duty_times_weekday = [eval(template_single_entry.format(start="04:00", end="06:30", cycle=25, position=0)),
                                eval(template_single_entry.format(start="11:45", end="19:30", cycle=25, position=1))]
    early_duty_times_weekend = [eval(template_single_entry.format(start="04:00", end="05:10", cycle=25, position=0)),
                                eval(template_single_entry.format(start="08:00", end="09:30", cycle=25, position=1)),
                                eval(template_single_entry.format(start="11:40", end="19:30", cycle=25, position=2))]
    late_duty_times_weekday = [eval(template_single_entry.format(start="05:50", end="12:30", cycle=25, position=0)),
                               eval(template_single_entry.format(start="17:30", end="19:30", cycle=25, position=1))]
    late_duty_times_weekend = [eval(template_single_entry.format(start="08:00", end="12:30", cycle=25, position=0)),
                               eval(template_single_entry.format(start="17:30", end="19:30", cycle=25, position=1))]
    night_duty_times_weekday = [eval(template_single_entry.format(start="05:50", end="06:30", cycle=25, position=0)),
                                eval(template_single_entry.format(start="11:40", end="19:30", cycle=25, position=1))]
    night_duty_times_weekend = [eval(template_single_entry.format(start="08:00", end="09:30", cycle=25, position=0)),
                                eval(template_single_entry.format(start="11:40", end="19:30", cycle=25, position=1))]
    weekday_times = [eval(template_single_entry.format(start="05:50", end="06:30", cycle=25, position=0)),
                     eval(template_single_entry.format(start="09:00", end="13:00", cycle=25, position=1)),
                     eval(template_single_entry.format(start="16:30", end="19:30", cycle=25, position=2))]
    weekend_times = [eval(template_single_entry.format(start="08:00", end="19:30", cycle=25, position=0))]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        if EARLY_DUTY_LABEL in event['summary']:
            early_duties.append(datetime.datetime.strptime(start, "%Y-%m-%d"))
        if LATE_DUTY_LABEL in event['summary']:
            late_duties.append(datetime.datetime.strptime(start, "%Y-%m-%d"))
        if NIGHT_DUTY_LABEL in event['summary']:
            night_duties.append(datetime.datetime.strptime(start, "%Y-%m-%d"))
    utc_now = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
    result = {}
    while utc_now < utc_end:
        day = utc_now.strftime("%a").lower()

        override = pathlib.Path("/overrides").joinpath(day)
        if override.exists():
            with override.open("r") as f_override:
                result[day] = json.load(f_override)
        else:
            if utc_now in early_duties:
                if day in ("sat", "sun"):
                    result[day] = early_duty_times_weekend
                else:
                    result[day] = early_duty_times_weekday
            elif utc_now in late_duties:
                if day in ("sat", "sun"):
                    result[day] = late_duty_times_weekend
                else:
                    result[day] = late_duty_times_weekday
            elif utc_now in night_duties:
                if day in ("sat", "sun"):
                    result[day] = night_duty_times_weekend
                else:
                    result[day] = night_duty_times_weekday
            elif day in ("sat", "sun"):
                result[day] = weekend_times
            else:
                result[day] = weekday_times
        print(f"{day}: {' | '.join(entry['start'] + '-' + entry['end'] for entry in result[day])}")
        utc_now += datetime.timedelta(days=1)
    return result


if __name__ == '__main__':
    main()
