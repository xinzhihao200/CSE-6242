import MySQLdb
import sndmsg
#from datetime import datetime
#from threading import Timer

#x = datetime.today()
#y = x.replace(day = x.day + 1, hour = 23, minute = 59, second = 0, microsecond = 0)
#We define the default sending time as 23:59 every day. Please be free to adjust
#the time if you want to see the instant coupon email

#delta_t = y - x

#secs = delta_t.seconds + 1

db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = " ",
                     db = "infodb")
cursor = db.cursor()

query1 = "select * from ((select restaurant, email from customers) as a left join (select restaurant, count(*) from customers group by restaurant) as b on a.restaurant = b.restaurant)"


cursor.execute(query1)
#cursor.execute(query2)
results = cursor.fetchall()
for row in results:
    sndmsg.snd(row[1],row[2],row[3])

query2 = "delete from customers"

cursor.execute(query2)
db.commit()
db.close()
print "Done!"


#t = Timer(secs, readandsend)
#t.start
#sq1 = "select email, restaurant from customers"



