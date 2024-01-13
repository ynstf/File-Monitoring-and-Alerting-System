import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv


def send_email_to(email_receiver, critical_file):
    # Load environment variables from .env file
    load_dotenv()

    # Define email sender and receiver
    email_sender = os.environ.get('EMAIL') #'write-email-here'
    email_password = os.environ.get('PWD') #'write-password-here'

    # Set the subject and body of the email
    subject = 'Critical File Change Notification'

    body = 'Hello, this is a custom message to inform you about a critical file change.'
    body += f'\nThe critical file {critical_file} has been modified. Please take immediate action.'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())