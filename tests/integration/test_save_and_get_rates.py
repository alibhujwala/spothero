import json
import os


def test_invalid_rates(client):
    response = client.post('/rates', json={'rates': [{'notvalid': '0'}]})
    assert response.status_code == 422
    assert response.json['error'] == "Rates don't contain all required information(days, times, tz, price)"


def test_valid_rates_cst(client):
    rates = get_valid_rates()
    start_datestring = '2015-07-01T07:00:00-05:00'
    end_datestring = '2015-07-01T12:00:00-05:00'

    post_response = client.post('/rates', json=rates)
    get_response = client.get(f'/rates?from={start_datestring}&to={end_datestring}')

    assert post_response.status_code == 200
    assert get_response.status_code == 200
    assert get_response.data == b'1750'


def test_valid_rates_utc(client):
    rates = get_valid_rates()
    start_datestring = '2015-07-04T15:00:00+00:00'
    end_datestring = '2015-07-04T20:00:00+00:00'

    _ = client.post('/rates', json=rates)
    response = client.get(f'/rates?from={start_datestring}&to={end_datestring}')

    assert response.status_code == 200
    assert response.data == b'2000'


def test_valid_rates_unavailable(client):
    rates = get_valid_rates()
    start_datestring = '2015-07-04T07:00:00+05:00'
    end_datestring = '2015-07-04T20:00:00+05:00'

    _ = client.post('/rates', json=rates)
    response = client.get(f'/rates?from={start_datestring}&to={end_datestring}')

    assert response.status_code == 200
    assert response.data == b'unavailable'


def test_valid_rates_timezone_spillover(client):
    rates = get_valid_rates()
    start_datestring = '2015-07-05T22:00:00-00:00'
    end_datestring = '2015-07-05T23:01:00-00:00'

    _ = client.post('/rates', json=rates)
    response = client.get(f'/rates?from={start_datestring}&to={end_datestring}')

    assert response.status_code == 200
    assert response.data == b'2000'


def get_valid_rates():
    myPath = os.path.dirname(os.path.abspath(__file__))
    rates = json.load(open(os.path.join(myPath,'../valid_rates.json'), 'r'))
    return rates