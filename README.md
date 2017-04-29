# CSE6242 Team 30 Final Project

## Project demo
[![Project demo](assets/demo.png)](https://www.youtube.com/watch?v=-jquTb80sXY&feature=youtu.be)

## Requirements
* Python 2.7
* Numpy
* MySQL, MySQLdb
* flask 0.12


## Import Database

Please make sure you have installed MySQL and MySQLdb before running the program! Please make sure the password of user 'root' is ' '. (a single space)

Download database.sql from [here](https://drive.google.com/open?id=0B2rvL2JjAe7kVVdIRkxTY216c2M), 
Then execute command:
```
$ mysql -u root -p alldata < alldata.sql
```

Import infodb.sql from `coupon.infodb.sql`:
```
$ mysql -u root -p infodb < infodb.sql
```

## Usage

Get to the root directory, run the following command:
```python
python connection.py

```

## Send coupon and delete coupon data

Change the directory to `coupon` folder and execute 
```
python readsql.py
```
This will read the record of request and send an email to every registered account with coupon, restaurant information and promotion. After that, it will delete all data in the database `infodb`.
