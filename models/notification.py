#!/usr/bin/python3
"""
Notification class
"""


from sqlalchemy import Column, String, ForeignKey, Enum
import models
from models.base_model import BaseModel, Base
import smtplib
from os import getenv
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


"""Load enviromental variable from .env file"""
load_dotenv()
class Notification(BaseModel, Base):
    """ Notification Representation"""

    if models.storage_t == 'db':
        __tablename__ = 'notification'

        reciever = Column(String(128), nullable=False)
        Message_content = Column(String(128), nullable=False)
        status = Column(Enum("Read", "Unread"))
        user_id = Column(String(128), ForeignKey("user.id"), nullable=False)


    def sendemail(self, sender, receiver, message_content):

        EA_NOTIFICATION_SENDER = getenv("EA_NOTIFICATION_SENDER")
        EA_NOTIFICATION_SENDER_PWD = getenv("EA_NOTIFICATION_SENDER_PWD")
        # Gmail SMTP server details
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587


        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Notification'
        msg.attach(MIMEText(message_content, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EA_NOTIFICATION_SENDER, EA_NOTIFICATION_SENDER_PWD)
            server.sendmail(sender, receiver, msg.as_string())








    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


