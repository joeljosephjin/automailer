import csv, smtplib, ssl, sys, traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yagmail
    
my_email = "joeljosephjin@gmail.com"   
subject="Request for Summer Research Opportunity"
   

#filename = "document.pdf"

def mimer(name,email,text_file="text.txt",html_file="html.txt"):
    sender_email = my_email
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    with open(text_file) as file:
        text = file.read()
        
    with open(html_file) as file:
        html = file.read()
    
    text = text.format(name=name)
    html = html.format(name=name)
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    #return message
    return html 


context = ssl.create_default_context()
with yagmail.SMTP(my_email) as yag:
    with open("contacts.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for a,b,c,d,name,email,e,f in reader:
            try:
                message=mimer(name,email)            
                #message = "<h1>Whaaaaaaaaaaaat</h1>"
                yag.send(
                    to=email,
                    subject=subject,
                    contents=message,
                    #contents="testing..."
                    #attachments=filename,
                )
            except:
                traceback.print_exc()
                break;
                
                
                
 

