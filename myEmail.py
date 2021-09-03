# myEmail.py

import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

def googleMail(addr, txt):
    host = "smtp.gmail.com"
    port = "587"

    senderAddr = "kumamyung@gmail.com"
    recipientAddr = addr

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "[공적 마스크 재고 조회] by ㅇㄷ?"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msg.attach(MIMEText(txt))

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("kumamyung@gmail.com", "narvash24234@!")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()


    