import smtplib
import generate
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def snd(user = "jcheng@gatech.edu", user2 = "Chineserestaurant", user4 = 1):
    fromaddr = "cse6242team30@gmail.com"
    toaddr = user
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your coupon!"

    coupon = generate.generate_code()
    body = "Hi! Your coupon is " + coupon + " for " + user2 + ", with promotion of %d people including you share the same coupon, the promotion will be %d percent off according to our calculation" % (user4, min(3*user4,20))
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "password321")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return

#if __name__ == '__main__':
#	main()

