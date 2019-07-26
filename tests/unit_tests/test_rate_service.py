from datetime import datetime

from rate_service import utc_standardized_date, to_military_time


def test_utc_standardized_rate_same_day():
    day_index = 0
    start_time = '0100'
    end_time = '0500'
    tz = 'America/Chicago'

    day_index, start_time, duration = utc_standardized_date(day_index, start_time, end_time, tz)

    assert day_index == 0
    assert start_time == 600
    assert duration == 400


def test_utc_standardized_rate_next_day():
    day_index = 0
    start_time = '2200'
    end_time = '2400'
    tz = 'America/Chicago'

    day_index, start_time, duration = utc_standardized_date(day_index, start_time, end_time, tz)

    assert day_index == 1
    assert start_time == 300


def test_utc_standardized_rate_previous_day():
    day_index = 0
    start_time = '0100'
    end_time = '0300'
    tz = 'Asia/Dubai'

    day_index, start_time, duration = utc_standardized_date(day_index, start_time, end_time, tz)

    assert day_index == 6
    assert start_time == 2100


def test_to_military():
    dt = datetime(2019, 7, 23, 20, 44, 38, 84288)

    military_time = to_military_time(dt)

    assert military_time == 2044
