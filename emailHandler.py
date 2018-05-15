import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


# http://naelshiab.com/tutorial-send-email-python/
def send_email(subject, file_path, file_name):

    fromaddr = "pythonnotification1@gmail.com"
    toaddr = "lud291@mail.usask.ca"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = "Python Notification"

    msg.attach(MIMEText(body, 'plain'))

    filename = file_name
    attachment = open(file_path, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "3rpjlSPVjcp8")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
