import smtplib
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def send_email(sender_email, recipient_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject 
    
    message.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('localhost', 25) as server:
        server.send_message(message)
        log.info(f"Email sent successfully to {recipient_email}")
    
if __name__ == "__main__":
    sender_email = "sender@localhost"
    recipient_email = "baray58394@ckuer.com"
    subject = "Local Test"

    body = """
        Hello,

        This is a test email sent from a local Docker SMTP server.
        
        Best regards,
        Local Email Sender
    """
    send_email(sender_email, recipient_email, subject, body)
