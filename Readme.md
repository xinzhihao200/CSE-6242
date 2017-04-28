DESCRIPTION:

INSTALLATION:

## Import Database
Download database.sql from [here](https://drive.google.com/open?id=0B2rvL2JjAe7kMUp6UTZNZTI3X00), 
then execute command:

$ mysql -u root -p alldata < database.sql
# We need to modify our database, because it has been changed
$ mysql -u root -p
mysql> alter table alldata.business add fulltext(name, categories, city);

## Import python 2.7.13 and required packages (mysql,flask)


EXECUTION:

Get to the root directory, run the following command:
$ python connection.py

If this does not work out, you might be missing Python or some libraries. 
Use "pip install {library_name}" to install. 
Open your browser, type "localhost:5000/welcome" to enter the welcome page.

Coupon part:
Please make sure you have installed MySQL and MySQLdb before running the program!
Change the directory to coupon folder and type "python readsql.py", and that will read the record of request and send an email to every registered account with coupon, restaurant information and promotion.
