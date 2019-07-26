### SpotHero Example App

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
$ python app.py
```
In flask, Default port is `5000`

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```
### Run flask for production

** Run with gunicorn **

In  spothero/
```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```
* -w : number of worker
* -b : Socket to bind
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
>>> requests.get("http://127.0.0.1:5000/rates?to=2015-07-01T07:00:00-05:00&from=2015-07-01T12:00:00-05:00")

u'1750'
````
Unavailable Request Example:
```
>>> requests.get("http://127.0.0.1:5000/rates?to=2015-07-01T07:00:00-05:00&from=2015-07-02T12:00:00-05:00").text
u'unavailable'
```
Bad Request Example: 
```angular2
>>> requests.get("http://127.0.0.1:5000/rates?to=2015-07-01T07:00:00-05:00&from=2015-07-01T12:00:").text
u'{"error":"start, end query parameters must be in valid ISO-8601 dates"}\n'
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
>>> requests.post('http://127.0.0.1:5000/rates', json={
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
>>> requests.post("http://127.0.0.1:5000/rates").text
u'{"error":"Payload must contain \\"rates\\" outer object"}\n'
>>> requests.post("http://127.0.0.1:5000/rates", json={"rates": [{'days': 'tues'}]}).text
u'{"error":"Rates don\'t contain all required information(days, times, tz, price)"}\n'
```

## Next Steps

Add DB layer to persist rates information.

Dockerize 


Add swagger API documentation 

Authentication, user sessions. 