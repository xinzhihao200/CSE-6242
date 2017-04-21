import MySQLdb
import sndmsg

db = MySQLdb.connect(host = "localhost",
                     user = "team30",
                     passwd = "team30",
                     db = "infodb")

cursor = db.cursor()

query = "SELECT * FROM customers"

cursor.execute(query)
results = cursor.fetchall()
for row in results:
    print row[1]
    sndmsg.snd(row[1])
db.close();
