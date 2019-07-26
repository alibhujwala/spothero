from datetime import datetime, timedelta

import dateutil.parser
import pytz

from invalid_data import InvalidData

weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
rates = {day_index: [] for day_index in range(7)}


def save_rate(payload):
    global rates
    validated_rates = validate_rate_payload(payload)
    rates = validated_rates


def get_rate(start_datestring, end_datestring):
    start_utc_datetime, end_utc_datetime = validate_dates(start_datestring, end_datestring)

    day_index = start_utc_datetime.weekday()
    start_military = to_military_time(start_utc_datetime)
    for rate in rates[day_index]:
        end_rate_datetime = start_utc_datetime + timedelta(minutes=rate['duration'])
        if rate['start_time'] <= start_military and end_utc_datetime <= end_rate_datetime:
            return rate['price']

    return 'unavailable'


def validate_rate_payload(payload):
    """validates json format, and transforms into rates['day_index'] dictionary"""
    if not payload or 'rates' not in payload:
        raise InvalidData('Payload must contain "rates" outer object')

    rates = {day_index: [] for day_index in range(7)}

    for rate in payload['rates']:
        try:
            days = rate['days']
            times = rate['times']
            tz = rate['tz']
            price = rate['price']

        except KeyError:
            raise InvalidData("Rates don't contain all required information(days, times, tz, price)")

        try:
            days = days.split(',')
            days = [day[0:3].lower() for day in days]
            days = [weekdays.index(day) for day in days]
        except:
            raise InvalidData("days contain invalid data format(mon:, tue:, wed:, thurs:, fri:, sat:, sun:")

        try:
            start_string, end_string = times.split('-')
        except:
            raise InvalidData("times contain invalid data format")

        if tz not in pytz.all_timezones:
            raise InvalidData(f"timezone must be a valid timezone({pytz.all_timezones})")

        for day_index in days:
            day_index, start_time, duration = utc_standardized_date(day_index, start_string, end_string, tz)
            rates[day_index].append({
                          'start_time': int(start_time),
                          'duration': duration,
                          'price': price
                          })

    return rates


def validate_dates(start_datestring, end_datestring):
    """validate and convert to python utc datetimes"""
    try:
        # + gets encoded to %2B which gets interperted as a space. Making conversion to allow client to send '+'
        start_utc_datetime = dateutil.parser.parse(start_datestring.replace(' ', '+')).astimezone(pytz.utc)
        end_utc_datetime = dateutil.parser.parse(end_datestring.replace(' ', '+')).astimezone(pytz.utc)
    except:
        raise InvalidData("from, to query parameters must be in valid ISO-8601 dates")

    if start_utc_datetime >= end_utc_datetime:
        raise InvalidData("to datetime must be after from datetime")

    return start_utc_datetime, end_utc_datetime


def to_military_time(datestring):
    return int(datestring.strftime('%H')) * 100 + int(datestring.strftime('%M'))


def utc_standardized_date(day_index, start_time, end_time, tz):
    """calculate utc offset, and convert to military time"""
    start_time, end_time = int(start_time), int(end_time)
    duration = end_time - start_time
    timezone = datetime.now(pytz.timezone(tz))
    offset = timezone.utcoffset().total_seconds() / 60 / 60
    start_time = start_time - int(offset) * 100
    if start_time < 0:
        start_time = start_time + 2400
        day_index = previous_day(day_index)
    elif start_time > 2400:
        start_time = start_time - 2400
        day_index = next_day(day_index)

    return day_index, start_time, duration


def next_day(day_index):
    return (day_index + 1) % 6


def previous_day(day_index):
    return day_index - 1 if day_index else 6
