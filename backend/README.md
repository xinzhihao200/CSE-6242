# Backend

## Import Database
Download database.sql from [here](https://drive.google.com/open?id=0B2rvL2JjAe7kMUp6UTZNZTI3X00), then execute command:

 ```
$ mysql -u root -p alldata < database.sql
# We need to modify our database, because it has been changed
$ mysql -u root -p
mysql> alter table alldata.business add fulltext(name, categories, city);

```

## Use Search

In `backend/recommender.py`, use function `easy_search`
```python
from backend.recommender import easy_search

string = 'chinese'
data = easy_search(string)
```
will return a list whose length is at most 100. Each element is a dictionary, like:
```
 {'address': [u'4350 N 19th Ave, Ste 4'],
  'attributes': [u'AcceptsInsurance: True', u'ByAppointmentOnly: True'],
  'business_id': [u'wkW_FjO6kIDOw61RsXtdeA'],
  'categories': [u'Health & Medical', u'Acupuncture'],
  'city': [u'Phoenix'],
  'hours': [u'Monday 9:0-16:30',
   u'Tuesday 9:0-16:30',
   u'Wednesday 9:0-16:30',
   u'Thursday 9:0-16:30',
   u'Friday 9:0-17:0',
   u'Saturday 9:0-13:0'],
  'is_open': 1,
  'latitude': 33.5002,
  'longitude': -112.1,
  'name': [u'Arizona Acupuncture & Chinese Medicine Clinic'],
  'neighborhood': None,
  'postal_code': [u'85015'],
  'price': None,
  'review_count': 5,
  'stars': 5.0,
  'state': [u'AZ']}
```
Most elements do not have `price`, so I just set to `None`.
