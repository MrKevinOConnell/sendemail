# -*- coding: utf-8 -*-
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import sys
import os
from dotenv import load_dotenv



class Founder:
  def __init__(self, firstName, domain,company):
    self.firstName = firstName
    self.domain = domain
    self.company = company

def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def checkIfSent(name,email,company):
    with open('sentemails.txt', 'r+') as sentemails:
        for sentline in sentemails:
            sentFounder = sentline.split()
            for l in sentFounder:
                finishSentFounder = l.split(',')
                doneEmail = finishSentFounder[1]
                doneCompany = finishSentFounder[2]
                if (doneCompany == company or doneEmail == email):
                    if (doneCompany == company):
                        print("You already sent an email to somebody at " + doneCompany + "!")
                        return True
                    elif (doneEmail == email):
                        print("You already sent an email to " + doneEmail + "!")
                        return True
        sentemails.write(name + ',' + email + ',' + company + '\n')
        return False
#example sendEmail('kevin','kevin@example.com','Student')
def sendEmail(x,y,z):

    envars = os.path.dirname('.env')
    load_dotenv(envars)
    upperCaseName = x.capitalize()
    email = os.getenv('EMAIL')
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = y
    msg['Subject'] = 'CS Student inquiring about opportunities at ' + z

    p1 = 'Hi ' + upperCaseName + ',<br><br>My name’s Kevin O’Connell. I’m a Sophomore at Marquette University studying Computer Science.'
    p2 = "<br><br>I recently finished up an SE internship with Charmed, a Techstars Boulder 2020 grad, in which I helped them launch <a href='https://apps.apple.com/us/app/keys-for-dating/id1510154956'>Keys for Dating</a>. <br><br>"
    p3 = "I'm also working on a text based life coaching app that uses GPT3 to help assist life coaches work with their clients. <br><br>"
    p4 = 'I saw your company ' + z + ', and wanted to send a quick email to say I love what you are working on. I’ve been looking for startups that I could help out and impact, and when I saw yours, I thought I would be a good fit.'
    p5 = '<br><br>With that being said, I was wondering if there are any ways I could get involved?'
    p6 ='<br><br>Most of my work has been in Swift and Javascript(React,React Native,Node, Redux), but I also know Java,C, and Python from school.'
    p7 = '<br><br>Attached is my resume if you’d like more context on my work experience. If you are interested in learning more about my work, I’d love to set up a call with you. Let me know some times that work in the afternoon on your end and I’ll make it work on my end.'
    end ='<br><br>Thanks,<br>Kevin'
    text = p1+ p2+p3+p4+p5+p6+p7+end
    msg.attach(MIMEText(text,'html'))
    file = '/Users/kevinoconnell/sendemail/KevinOConnellResume.pdf'
    part = MIMEApplication(
                open(file, "rb").read(),
                Name=basename(file)
                )
            # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)
    send = smtplib.SMTP('smtp-mail.outlook.com',587)
    send.ehlo()
    send.starttls()
    send.login(email, os.getenv('PASSWORD'))
    send.sendmail(email, y, msg.as_string())
    send.close()
if len(sys.argv)== 2:
    if(sys.argv[1] == 'r'):
        emails = open("emails.txt", "r")
        Lines = emails.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            print("Founder {}: {}".format(count, line.strip()))
    elif (sys.argv[1] == 's'):
        with open("emails.txt") as emails:
            for line in emails:
                founder = line.split()
                for l in founder:
                    finishFounder = l.split(',')
                    if(len(finishFounder)>3):
                        raise Exception("too many arguments!")
                    firstName = finishFounder[0]
                    domain = finishFounder[1]
                    company = finishFounder[2]
                    email = firstName + domain
                    check = checkIfSent(firstName,email,company)
                    if(check == False):
                        sendEmail(firstName,email,company)
                        print("Email sent to " + firstName + "!")
        open("emails.txt", "w").close()
    elif (sys.argv[1] == 'test'):
        #check = checkIfSent('kevin','kevinoconnell42@gmail.com','student')
        #if(check == False):
        sendEmail('kevin','kevinoconnell42@gmail.com','student')
        print("Email sent to " + 'kevin' + "!")
    elif (sys.argv[1] == 'testlist'):
        with open("emails.txt") as emails:
            for line in emails:
                founder = line.split()
                for l in founder:
                    finishFounder = l.split(',')
                    if(len(finishFounder)>3):
                        raise Exception("too many arguments!")
                    firstName = finishFounder[0]
                    domain = finishFounder[1]
                    company = finishFounder[2]
                    email = firstName + domain
                    print(email)
    elif (sys.argv[1] == 'checksent'):
        with open('sentemails.txt', 'r') as sentemails:
            Lines = sentemails.readlines()
            count = 0
            # Strips the newline character
            for line in Lines:
                count += 1
                print("Founder {}: {}".format(count, line.strip()))
    elif (sys.argv[1] == 'h'):
        print('Commands:\n')
        print('*firstName* *domain* *Company*: adds a entry to the list, where *text* is what you enter in\n')
        print('r: reads the list of founders that will be sent a email\n')
        print('s: sends a email to founders that you have not yet sent emails to\n')
        print('test: tests the checkIfSent function\n')
        print('checksent: checks who has been emailed')
    else:
        print('not a valid command, enter in h to see the list of commands avaliable!')
if len(sys.argv)>3:
    founder = Founder(sys.argv[1],sys.argv[2],sys.argv[3])
    string = founder.firstName + ','+ founder.domain + ','+founder.company + '\n'
    if is_non_zero_file('emails.txt'):
        emails = open("emails.txt", "a")
        emails.write(string)
    else:
        emails = open("emails.txt", "w+")
        emails.write(string)