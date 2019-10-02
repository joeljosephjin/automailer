import csv, smtplib, ssl, sys, traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yagmail
import getpass
    
my_email = "joeljosephjin@gmail.com"   
subject="Request for Summer Research Opportunity"
password = getpass.getpass(prompt='Password: ', stream=None)  

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
    
    return message 

new_contacts = list()
    
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(my_email, password)
    with open("contacts.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for rank,univ,link,labn,name,email,mailed,replied in reader:
            if mailed=="No":    
                try:
                    message=mimer(name,email)            
                    server.sendmail(
                        my_email,
                        email,
                        message.as_string(),
                    )
                    mailstate="Yes" 
                except:
                    #traceback.print_exc()
                    mailstate="No"
                    #break;
                new_contacts.append({'CSRankings':rank,'University':univ,'Link':link,'Lab Name':labn,'Name':name,'Email':email,'Mailed?':mailstate,'Replied?':replied})

#print(new_contacts)                
with open('new_contacts.csv', 'w') as csvfile:
    fieldnames = ['CSRankings','University','Link','Lab Name','Name','Email','Mailed?','Replied?']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(new_contacts)
    
    
print("Writing complete")                    
                    