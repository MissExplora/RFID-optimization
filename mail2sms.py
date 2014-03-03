import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

def sendmail(subject, to_addr, message):
    '''
    Send a mail.
    '''
    global user, passw, server
    port = 25

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.add_header('From', user)
    msg.add_header('To', to_addr)

    msg.attach(MIMEText(message))
    connection = smtplib.SMTP(server, port)
    connection.ehlo(server)
    connection.starttls()
    connection.ehlo(server)
    connection.login(user, passw)

    print connection.sendmail(msg['From'], to_addr, msg.as_string())
    return connection.close()


if __name__ == "__main__":
    server = ''
    port = 0
    user = ''
    passw = ''
    for i requests.get("http://127.0.0.1:8080/pinkiji").json():
        if i["count"]>12:
            sendmail("Potrebna promjena na blagajni %s"i["blagajna"],ADRESA_MAIL2SMS,
                "Potrebna promjena na blagajni %s"i["blagajna"])
        time.sleep(60)

