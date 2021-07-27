import time
from datetime import timedelta
import smtplib
import configparser
from email.message import EmailMessage

start_time = time.monotonic()
config = configparser.ConfigParser()
config.read('credentials.ini')

mail = config['Email']['mail']
passwd = config['Email']['passwd']

msg = EmailMessage()
msg['Subject'] = 'Bought or sold CE/PE'
msg['From'] = mail
msg['To'] = mail
msg.set_content('get the logging files')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(mail, passwd)
    smtp.send_message(msg)

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))