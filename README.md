### SpotHero Example App

Live Example App: http://bhuj2000.pythonanywhere.com
## Installation

Supports python 3.6+

Recommended: Create virtual ENV

Install with pip:

```
$ pip install -r requirements.txt
```

## Run Flask
### Run flask for develop
```
(spothero) ➜  spothero git:(master) ✗ python app.py 
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

## Testing
** Run in terminal **

```
$ python -m pytest tests/
```

** Run in pycharm **

CMD + , => Tools -> Python Integrated Tools -> Testing => Default test runner -> pytest

Right click /tests, or test_*.py, or function and run with pytest.
# API DOCUMENTATION

 Endpoints
 
`/rates`

ALLOWED HTTP REQUESTS:

#### GET:
Parameters: TO, FROM; Valid ISO-8601

##### Responses:


200: $rate, or unavailable


422: Error parsing parameters


Available Request Example: 

```
>>> requests.get("http://bhuj2000.pythonanywhere.com/rates?from=2015-07-01T07:00:00-05:00&to=2015-07-01T12:00:00-05:00").text
u'1750'
>>> requests.get("http://bhuj2000.pythonanywhere.com/rates?from=2015-07-04T15:00:00+00:00&to=2015-07-04T20:00:00+00:00").text
u'2000'
````
Unavailable Request Example:
```
>>> requests.get("http://bhuj2000.pythonanywhere.com/rates?from=2015-07-01T12:00:00-05:00$to=2015-07-03T07:00:00-05:00").text
u'unavailable'
```
Bad Request Example: 
```
>>> requests.get("http://bhuj2000.pythonanywhere.com/rates?to=2015-07-01T07:00:00-05:00&from=2015-07-01T12:00:").text
u'{"error":"from, to query parameters must be in valid ISO-8601 dates"}\n'
>>> requests.get("http://127.0.0.1:5000/rates?to=2015-07-01T07:00:00-05:00&from=2015-07-02T12:00:00-05:00").text
u'{"error":"to datetime must be after from datetime"}\n'
```

#### POST:

REQUIRED HEADERS: application/json

Payload Example: 
```
{
  "rates": [
    {
      "days": "mon,tues,thurs",
      "times": "0900-2100",
      "tz": "America/Chicago",
      "price": 1500
    }, {
      "days": "fri,sat,sun",
      "times": "0900-2100",
      "tz": "America/Chicago",
      "price": 2000
    }, {
      "days": "wed",
      "times": "0600-1800",
      "tz": "America/Chicago",
      "price": 1750
    }, {
      "days": "mon,wed,sat",
      "times": "0100-0500",
      "tz": "America/Chicago",
      "price": 1000
    }, {
      "days": "sun,tues",
      "times": "0100-0700",
      "tz": "America/Chicago",
      "price": 925
    }
  ]
}
```

##### Responses
200: Saved Rate


422: Invalid payload

##### Examples:
Valid Payload:

```
>>> requests.post('http://bhuj2000.pythonanywhere.com/rates', json={
...   "rates": [
...     {
...       "days": "mon,tues,thurs",
...       "times": "0900-2100",
...       "tz": "America/Chicago",
...       "price": 1500
...     }, {
...       "days": "fri,sat,sun",
...       "times": "0900-2100",
...       "tz": "America/Chicago",
...       "price": 2000
...     }, {
...       "days": "wed",
...       "times": "0600-1800",
...       "tz": "America/Chicago",
...       "price": 1750
...     }, {
...       "days": "mon,wed,sat",
...       "times": "0100-0500",
...       "tz": "America/Chicago",
...       "price": 1000
...     }, {
...       "days": "sun,tues",
...       "times": "0100-0700",
...       "tz": "America/Chicago",
...       "price": 925
...     }
...   ]
... }
... )
<Response [200]>
```

Invalid Payload 

```
>>> requests.post("http://bhuj2000.pythonanywhere.com/rates").text
u'{"error":"Payload must contain \\"rates\\" outer object"}\n'
>>> requests.post("http://bhuj2000.pythonanywhere.com/rates", json={"rates": [{'days': 'tues'}]}).text
u'{"error":"Rates don\'t contain all required information(days, times, tz, price)"}\n'
```

## Next Steps

Add DB layer to persist rates information.

Dockerize 


Add swagger API documentation 

Authentication, user sessions.