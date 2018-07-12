# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:58:07 2018

@author: ahmet.kuzucuoglu
"""

import smtplib

#1. Creating an smtp object out of smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

    type(smtpObj)

#2. Handshaking with smtp library
smtpObj.ehlo()

#3. Starting TLS Encryption
smtpObj.starttls()


#4. Logging into SMTP Server
smtpObj.login('lamberson.sideprojects@gmail.com',input())  

#5. Sending an email
smtpObj.sendmail('lamberson.sideprojects@gmail.com','ahmetkuzucuoglu@gmail.com','Subject: Hello Ahmet.\nHow are you doing? ')

smtpObj.quit

smtpObj.sendmail