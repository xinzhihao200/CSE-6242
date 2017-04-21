import smtplib
import generate
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def snd(user = "jcheng@gatech.edu"):
    fromaddr = "cse6242team30@gmail.com"
    toaddr = user
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your coupon!"

    coupon = generate.generate_code()
    body = "Your coupon is " + coupon + ", with promotion of 30%!"
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

