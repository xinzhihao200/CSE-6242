Install mysql and mysqldb before using. MySQLdb is currently unavailable for python 3.3, you can use mysql connector if you want.

After customer request coupon, the local database should be named "infodb", with root passwd "123" and new user "team30" with password "team30".

The table has the name "customers", with three column "username", "email" and "restaurant", we will read the information in column "email" and send our coupon.

generate.py: Generating 8-digit coupon using SHA1.

sndmsg.py: Using google smtp server to send email automatically, default receiver is jcheng@gatech.edu.

sql.py: Read the database table, passing value into sndmsg.py for every record.

Running method: import sql.py in idle and run

Additional function: add timer to sql.py, making it do the job at 11:59 pm every day.
