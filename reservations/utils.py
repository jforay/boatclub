from django.core.mail import send_mail
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import base64
def send_res_email(user,boat,reservation_date,reseravtion_time):
    subject = f'{user.first_name} {user.last_name}\'s Destination Boat Club Confirmation on {reservation_date}'
    message = f'Hello {user.first_name}, \n\nYou have succesfully reserved {boat.name} on {reservation_date} at {reseravtion_time}.\n\n\nThank you and see you soon!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]#, 'DBCConfirmations@gmail.com']
    send_mail(subject,message,email_from,recipient_list)

def send_float_plan(user, boat, float_plan):
    subject = f'{user.first_name} {user.last_name}\'s Float Plan for {float_plan.reservation.date}'
    message = f"{user.first_name} {user.last_name}\'s Float Plan:\nDeparture Time: {float_plan.departure_time.strftime('%H:%M')}\nReturn time: {float_plan.return_time.strftime('%H:%M')}\nEmergency Contact: {float_plan.emergency_contact_name} ({float_plan.emergency_contact_phone})\nGuests: {float_plan.guests}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['DBCFloatPlans@gmail.com']
    send_mail(subject,message,email_from,recipient_list)


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_reservation_email(user, reservation_date, reservation_time, boat):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    message_text = f'Hello {user.first_name}, \n\nYou have successfully reserved {boat.name} on {reservation_date} at {reservation_time}.\n\n\nThank you and see you soon!'
    subject = f'{user.first_name} {user.last_name}\'s Destination Boat Club Confirmation on {reservation_date}'
    message = MIMEText(message_text)
    message['to'] = user.email
    message['from'] = "joe4a83@gmail.com"
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = build('gmail','v1',credentials=creds)
    sent_message = service.users().messages().send(userId="me", body={'raw':raw}).execute()
    return sent_message['id']

def send_float_plan_email(user, float_plan):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    message_text = f"{user.first_name} {user.last_name}\'s Float Plan:\nDeparture Time: {float_plan.departure_time.strftime('%H:%M')}\nReturn time: {float_plan.return_time.strftime('%H:%M')}\nEmergency Contact: {float_plan.emergency_contact_name} ({float_plan.emergency_contact_phone})\nGuests: {float_plan.guests}"
    subject = f'{user.first_name} {user.last_name}\'s Float Plan for {float_plan.reservation.date}'
    message = MIMEText(message_text)
    message['to'] = "joe4a83@gmail.com"
    message['from'] = "joe4a83@gmail.com"
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = build('gmail','v1',credentials=creds)
    sent_message = service.users().messages().send(userId="me", body={'raw':raw}).execute()
    return sent_message['id']


def send_float_plan_email_with_pdf(user, pdf_path):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    message_text = f"{user.first_name} {user.last_name}\'s Float Plan: Attached."
    subject = f'{user.first_name} {user.last_name}\'s Signed Float Plan'
    message = MIMEMultipart()
    message['to'] = "joe4a83@gmail.com"
    message['from'] = "joe4a83@gmail.com"
    message['subject'] = subject

    message.attach(MIMEText(message_text, 'plain'))
        # Attach the PDF file
    try:
        with open(pdf_path, 'rb') as attachment:
            mime_part = MIMEBase('application', 'octet-stream')
            mime_part.set_payload(attachment.read())

        # Encode the file in base64
        encoders.encode_base64(mime_part)
        mime_part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(pdf_path)}',
        )
        message.attach(mime_part)
    except FileNotFoundError:
        raise Exception(f"Error: PDF file not found at {pdf_path}")
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = build('gmail','v1',credentials=creds)
    try:
        sent_message = service.users().messages().send(
            userId="me", body={'raw': raw}
        ).execute()
        return sent_message['id']
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")

# def send_float_plan_email_with_pdf(user, pdf_path):
#     if not os.path.isfile(pdf_path):
#         raise Exception(f"Error: PDF file not found at {pdf_path}")
    
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     message_text = f"{user.first_name} {user.last_name}\'s Float Plan: Attached."
#     subject = f'{user.first_name} {user.last_name}\'s Signed Float Plan'
#     message = MIMEMultipart()
#     message['to'] = "joe4a83@gmail.com"
#     message['from'] = "joe4a83@gmail.com"
#     message['subject'] = subject

#     message.attach(MIMEText(message_text, 'plain'))

#         # Attach the PDF file
#     try:
#         with open(pdf_path, 'rb') as attachment:
#             mime_part = MIMEBase('application', 'pdf')
#             mime_part.set_payload(attachment.read())

#         # Encode the file in base64
#         encoders.encode_base64(mime_part)
#         mime_part.add_header(
#             'Content-Disposition',
#             f'attachment; filename={os.path.basename(pdf_path)}',
#         )
#         message.attach(mime_part)
#     except FileNotFoundError:
#         raise Exception(f"Error: PDF file not found at {pdf_path}")
    
#     raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

#     service = build('gmail','v1',credentials=creds)
#     try:
#         sent_message = service.users().messages().send(
#             userId="me", body={'raw': raw}
#         ).execute()
#         return sent_message['id']
#     except Exception as e:
#         raise Exception(f"Error sending email: {str(e)}")