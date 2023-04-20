import smtplib, ssl
import random
import requests
import schedule
import time
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
 
def getpoem(): 
    url = "http://poetrydb.org/title" 
    try: 
        data = requests.get(url).json()["titles"]
        purl = url +"/" +data[random.randint(0,3009)]
        poem = requests.get(purl).json()
        title = poem[0]["title"]
        author = poem[0]["author"]
        lines = poem[0]["lines"]
        p = "</br>"

        for i in range(0,len(lines)):
            p += (lines[i]) + "</br>"


        return title,author,p

    except Exception as e:
        print(e)

def sendEmail():
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = ""#email@email.com
    password = ""#Add password here
    receiver = ["",""]#List of emails 

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)

        title, author, poem = getpoem()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver)

        html =  """\
                <html>
                <head></head>
                <body>
                    <TT>
                    """+ poem + """</br>-"""+ author+"""
                    </TT>
                </body>
                </html> 
                """

        msg.attach(MIMEText(html, 'html'))

        server.sendmail(sender_email, receiver, msg.as_string())
        print("Message sent!")
    except Exception as e:
        print(e)
    finally:
        server.quit()

schedule.every().day.at("21:00").do(sendEmail)

while True:
     schedule.run_pending()
     time.sleep(1)
