# Viessmann Circular Pump Calendar

This tool can be used to control the Viessmann circular pump and set the schedule according to certain recurring appointments in a Google Calendar.
This saves a lot of energy. In my case it was that my wife works in early, late and night duty and we can drastically reduce the working times of the circular pump according to the duty times.
I execute it as a cron job every night using the Docker image.

## Prerequisites

* You must own a Viessmann device including Vitoconnect
* FHEM has been set up and the Vitoconnect device has been added using the [vitoconnect](https://wiki.fhem.de/wiki/Vitoconnect) module

## Obtain service account JSON and find Google Calendar subject

### Obtain service account JSON
1. Go to the [Google API Console](https://console.cloud.google.com/apis/dashboard) and register if necessary
2. Create a project if none exists
3. Open `credentials` tab, then `Create credentials` and choose `Service Account`.
4. Choose an ID, continue and select Owner Role
5. Copy the email address
6. Click on the email and open the Keys tab
7. Choose `Add Key`, then `Create new key` and `JSON` as type. The key is downloaded automatically. Store it in the project folder and name it service_account.json

### Find Google Calendar subject and add service account
1. Open [Google Calendar](https://calendar.google.com) and login
2. Click on the three dots next to the calendar you want to use and open Properties
3. Find the Share options and add a person
4. Enter the email copied from the service account and apply
5. Search for Calendar ID and copy it. (Format: xxx[...]xxx@group.calendar.google.com)

## Environment variables

This script uses environment variables. All variables are mandatory using the Python script, some variables have a default value when using the Docker container.

| **Variable name**       | **Example value**                                   | **Docker default** | **Description**                                       |
|-------------------------|-----------------------------------------------------|--------------------|-------------------------------------------------------|
| GOOGLE_SUBJECT          | crcqk3f5jvavvvvacccscfvos@group.calendar.google.com |                    | Subject of Google Calendar (follow README to find it) |
| FHEM_IP                 | 192.168.1.5                                         |                    | IP of FHEM server                                     |
| FHEM_VITOCONNECT_OBJECT | vitoconnect                                         | vitoconnect        | Name of Vitoconnect object in FHEM                    |
| EARLY_DUTY_LABEL        | Early duty                                          | Anja Frühdienst    | Label of the Google event for early duty (substring)  |
| LATE_DUTY_LABEL         | Late duty                                           | Anja Spätdienst    | Label of the Google event for late duty (substring)   |
| NIGHT_DUTY_LABEL        | Night duty                                          | Anja Nachtdienst   | Label of the Google event for night duty (substring)  |
| HOTWATER                | 1                                                   | 0                  | Set times for hot water production                    |

## Hot water

The times of hot water production can as well be set using this script. It can be enabled by setting the `HOTWATER` environment variable to `1`. This will start hot water production one hour earlier than circular pump and end at 10 PM every day.

## Overrides

Sometimes you might want to add an override value for one or multiple days. Maybe when you are on holidays or anything is different from the usual behaviour. In this case it is possible to add override files to the `/overrides` folder and mount it to the Docker container. The file must have the same name as the abbreviated week day (sat, sun etc). If a matching file for the week day exists, the content will be used.

Each file must contain a valid JSON string in a format like this:
```[{"mode":"5/25-cycles","position":0,"start":"08:00","end":"17:30"}]```

It is also possible to override the default times for the schedule. Content is the same as a day override (JSON string). Valid filenames are
* `early_duty_times_weekday`
* `early_duty_times_weekend`
* `late_duty_times_weekday`
* `late_duty_times_weekend`
* `night_duty_times_weekday`
* `night_duty_times_weekend`
* `weekday_times`
* `weekend_times`

## Docker example usage

```docker run -it -v /home/alex/viessmannCalendar/service_account.json:/app/service_account.json -v -v /home/alex/viessmannCalendar/overrides:/overrides -e GOOGLE_SUBJECT="crcqk3f5jvavvvvacccscfvos@group.calendar.google.com" -e FHEM_IP="192.168.1.5" --rm alexalex89/viessmann-circular-pump-calendar```