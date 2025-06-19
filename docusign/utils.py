# docusign/utils.py

import jwt
import requests
import time
import base64
from docusign_esign import RecipientViewRequest, ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, Tabs, Text, SignHere
import os
from django.conf import settings
from django.core.files.base import ContentFile

# Replace these with your actual values
INTEGRATION_KEY = "fc263be6-5a01-46c5-b9d3-4312a0719612"
USER_ID = "caf3bb2b-fd92-4673-87a9-9ab6d56009d8"
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAsPt+snvLhrXxDfTF3A+BEdkR2dlAcfEIk715kNKHwWufgIvQ
7QNodKOYtJdrZmT3AN3u6R4+fCHKfLEEhEfN97F83S0GcB0YFuI7Mp2MUN4IpZzC
UzTJCBtDZWIY495CiWogzOqF4kpYKAil/E7o5MlXqChctCKVMoydGDjj04J1NIFf
GznBFesXCpRVX6AAwi95U2piMe759cufm2TQSSAN7LSOZOitO6tokbQZ7XdlLaBW
6TuK8WC6tIS3jKQ22m0mpJ14FgDM0YU0W8PvnYWr9cICh5wk398gGIB4l6uIJa6r
HxSxAUVWBkHEMyb+W+ftCpskvC+w9LJCe0LxbQIDAQABAoIBACBJKNI/kh/XhguB
OS0NaQLMAh0nLEH88g8dlBUuytQmoXjOSMVMB1yr0Xo0W0PZLFQsqF4/ha+YbHt1
wXiuLq0+ZCRnB9MhA5l9GMaBhizkbFhl8e9C5F+FtbRDgn3jOGkgAq7PI7Bl1pIr
Dbiq3oKKFmMXRd4YpvYLP8dA7ZLSXa6mcdOVk3GprbF6VasXB2KUGQf8qs/Rk6vT
IRXdi1lpsbji8ck/jrj+l+H2Wqj40IA9HUmr8PoflB7xy91mgTLTwPTryXVC4rVs
E3w5qNDkDuAkdYr2Vl/6b+0lcKp6iz6DDVaLr0AqeXzHQmTc/3WR3hDn/qKm+kCS
DNpcXQMCgYEA9ymrQ/kKnEE9eKHqdn3vsaB06Dtb/9d5py2Zc6jZUDXm2/ecPFUj
Ajvw1QOVdjXX1KEuqv+FqXLzr6F0nuG7KkkmEQmQqWUzYXSvgJS1jDcJ4uouLuBy
lhDPN3fFn1zWJVhV3FHgQAb8GqjhgMgwNnNz829o7aJuTXO0dsfCvbMCgYEAt09z
ZM2uTYVENPrZBLK3NF0QWAb27kvuoHK4eWs5bm6RuSUexdYOtRrJqg8KbFu95Xhr
r6SxOyiHDfQ4N5rVCWmniDEznt0/dtrMwPNd5JUR1FNQTDgWGN8VOJpG3BnSQUIE
wVztOhbeA9jIdvohwpMl/KbVKlBl+BM74jJ5RF8CgYEAu+hJFe9jurH66ximaZmL
Ps8PsnNWmWaXTZtkW8NWHB4uurNAa7oKWKt7iGcmHW4H/dbg5Q5I7y++xpsIT7as
FhTwxOkxuyd+baxJtYbZk5VQhdymaesoEqEK+U+sxmDNSi0jcdIpnGPzDM2yS7dm
uC8ES2I7MtdX5rh9zgRHMPMCgYEAjgR57EEFp312CG3HsMIc+e6X+Pr8WEZvy9LV
ZQxTZGE5eO1vV+qtXlYwoxYgBy9UgfG3zE6WGLUfXQo2e63zGuXGK9einJPg1V5S
f7KMrcloFM2vSj2xsPc0Y7Py7hb7NB/Hu18ZU4Xf368WMEc93JdQONuwDqZXOcj8
/hQIq5UCgYBsjLpJ/EvkxXrCn5FxQVhZblKaGin2MzS0dRCeT4cLag/cisEnsZin
Gofyqmc4vytMdacxly9c4376XG+xZYOtw9AHRtlW6nKX/DIVltrRWAd0C/rO+9vf
r+KJoGkXJkC1x1gSliGr9lJJ0FrJiFH42ZzHnZTisPNdY+hbhRhgNw==
-----END RSA PRIVATE KEY-----"""
AUTH_BASE_URL = "https://account-d.docusign.com/oauth/token"  # Sandbox environment
DOCUSIGN_API_BASE_URL = "https://demo.docusign.net/restapi"
API_ACCOUNT_ID = "4ce66269-9bec-4729-8aff-96d38de6c5a4"


def generate_access_token():
    current_time = int(time.time())
    payload = {
        "iss": INTEGRATION_KEY,
        "sub": USER_ID,
        "aud": "account-d.docusign.com",
        "iat": current_time,
        "exp": current_time + 3600,  # Token expires in 1 hour
        "scope": "signature impersonation",
    }

    jwt_token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt_token}
    response = requests.post(AUTH_BASE_URL, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def send_docusign_envelope(recipient_email, recipient_name):
    """Send a float plan envelope using DocuSign."""
    try:
        # Generate access token
        access_token = generate_access_token()

        # Set up DocuSign API client
        api_client = ApiClient()
        api_client.host = DOCUSIGN_API_BASE_URL
        api_client.set_default_header("Authorization", f"Bearer {access_token}")

        print("loading pdf file...")
        # Load your PDF file
        with open("docusign/static/pdf/Float_plan_blank_docusign.pdf", "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        print('pdf load complete')
        # Define the document
        document = Document(
            document_base64=pdf_base64,
            name="Float Plan",
            file_extension="pdf",
            document_id="1"
        )

        # Define the signer
        signer = Signer(
            email=recipient_email,
            name=recipient_name,
            recipient_id="1",
            client_user_id="123"
        )

        # Define fields using anchor tags
        text_name = Text(
            anchor_string="Anchor_For_Name",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Name"
        )
        text_number = Text(
            anchor_string="Anchor_for_Number",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Number"
        )
        text_emergency_contact = Text(
            anchor_string="Anchor_For_Emergency_Contact",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="180",
            height="20",
            tab_label="Emergency Contact"
        )
        text_date = Text(
            anchor_string="Anchor_For_Departing_Date_Time",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="return date/time"
        )
        text_time = Text(
            anchor_string="Anchor_for_return_time",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Return Time"
        )
        text_emergency_contact_number = Text(
            anchor_string="Anchor_For_Emergency_Contact_Number",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Emergency Number"
        )
        text_guest1 = Text(
            anchor_string="Anchor_For_Guest_1",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Guest1",
            required=False,
        )
        text_guest2 = Text(
            anchor_string="Anchor_For_Guest_2",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Guest2",
            required=False,
        )
        text_guest3 = Text(
            anchor_string="Anchor_For_Guest_3",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Guest3",
            required=False,
        )
        text_guest4 = Text(
            anchor_string="Anchor_For_Guest_4",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Guest4",
            required=False,
        )
        text_guest5 = Text(
            anchor_string="Anchor_For_Guest_5",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="200",
            height="20",
            tab_label="Guest5",
            required=False,
        )
        text_guest6 = Text(
            anchor_string="Anchor_For_Guest_6",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest6",
            required=False,
        )
        text_guest7 = Text(
            anchor_string="Anchor_For_Guest_7",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest7",
            required=False,
        )
        text_guest8 = Text(
            anchor_string="Anchor_For_Guest_8",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest8",
            required=False,
        )
        text_guest9 = Text(
            anchor_string="Anchor_For_Guest_9",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest9",
            required=False,
        )
        text_guest10 = Text(
            anchor_string="Anchor_For_Guest_10",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest10",
            required=False,
        )
        text_guest11 = Text(
            anchor_string="Anchor_For_Guest_11",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest11",
            required=False,
        )
        text_guest12 = Text(
            anchor_string="Anchor_For_Guest_12",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest12",
            required=False,
        )
        text_guest13 = Text(
            anchor_string="Anchor_For_Guest_13",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest13",
            required=False,
        )
        text_guest14 = Text(
            anchor_string="Anchor_For_Guest_14",
            anchor_units="pixels",
            anchor_x_offset="-5",
            anchor_y_offset="0",
            width="220",
            height="20",
            tab_label="Guest14",
            required=False,
        )
        sign_here = SignHere(
            anchor_string="/signature/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )

        signer.tabs = Tabs(text_tabs=[text_name,text_number,text_emergency_contact,text_date,text_time,text_emergency_contact_number,text_guest1,text_guest2,text_guest3,text_guest4,text_guest5,text_guest6,text_guest7,text_guest8,text_guest9,text_guest10,text_guest11,text_guest12,text_guest13,text_guest14], sign_here_tabs=[sign_here])
        print("creating envelope")
        # Create the envelope
        envelope_definition = EnvelopeDefinition(
            email_subject="Please complete and sign the Float Plan",
            documents=[document],
            recipients={"signers": [signer]},
            status="sent"
        )        
    
        # Send the envelope
        envelopes_api = EnvelopesApi(api_client)

            # Debugging EnvelopesApi class
        print("Type of EnvelopesApi:", type(envelopes_api))
        print("Calling create_envelope now...")
        envelope_summary = envelopes_api.create_envelope(account_id=API_ACCOUNT_ID,envelope_definition=envelope_definition)

        return envelope_summary.envelope_id
    except Exception as e:
        raise Exception(f"Error sending envelope: {str(e)}")
    
# docusign/utils.py

def generate_signing_url(envelope_id, user):
    """Generate a signing URL for the user."""
    try:
        # Generate access token
        access_token = generate_access_token()

        # Set up DocuSign API client
        api_client = ApiClient()
        api_client.host = DOCUSIGN_API_BASE_URL
        api_client.set_default_header("Authorization", f"Bearer {access_token}")

        # Create recipient view request
        recipient_view_request = RecipientViewRequest(
            authentication_method="None",
            client_user_id="123",  # Same as in send_docusign_envelope
            recipient_id="1",
            return_url=f"http://127.0.0.1:8000/users/{user.id}/?envelope_id={envelope_id}",  # Redirect after signing
            user_name=f"{user.first_name} {user.last_name}",
            email=user.email,
        )

        # Generate the signing URL
        envelopes_api = EnvelopesApi(api_client)
        signing_url = envelopes_api.create_recipient_view(account_id=API_ACCOUNT_ID, envelope_id=envelope_id, recipient_view_request=recipient_view_request)
        return signing_url.url

    except Exception as e:
        raise Exception(f"Error generating signing URL: {str(e)}")



def save_completed_pdf(envelope_id, reservation):
    """Retrieve and save the completed PDF from DocuSign."""
    try:
        # Generate access token
        access_token = generate_access_token()

        # Set up DocuSign API client
        api_client = ApiClient()
        api_client.host = DOCUSIGN_API_BASE_URL
        api_client.set_default_header("Authorization", f"Bearer {access_token}")

        # Set up the Envelopes API
        envelopes_api = EnvelopesApi(api_client)
        signed_pdf = envelopes_api.get_document(account_id=API_ACCOUNT_ID, envelope_id=envelope_id, document_id='1')

        pdf_file_name = f"Signed_Float_plan_{reservation.id}.pdf"
        reservation.float_plan_pdf.save(pdf_file_name, ContentFile(signed_pdf),save=True)

    except Exception as e:
        raise Exception(f"Error fetching signed PDF: {str(e)}")
        

# def save_completed_pdf(envelope_id, reservation):
#     """Retrieve and save the completed PDF from DocuSign."""
#     try:
#         # Generate access token
#         access_token = generate_access_token()

#         # Set up DocuSign API client
#         api_client = ApiClient()
#         api_client.host = DOCUSIGN_API_BASE_URL
#         api_client.set_default_header("Authorization", f"Bearer {access_token}")

#         # Set up the Envelopes API
#         envelopes_api = EnvelopesApi(api_client)
#         signed_pdf = envelopes_api.get_document(account_id=API_ACCOUNT_ID, envelope_id=envelope_id, document_id='1')
#         print('checking pdf')
#         with open(f"debug_Signed_Float_plan_{reservation.id}.pdf", "wb") as debug_file:
#             debug_file.write(signed_pdf)
#         pdf_file_name = f"Signed_Float_plan_{reservation.id}.pdf"
#         reservation.float_plan_pdf.save(pdf_file_name, ContentFile(signed_pdf),save=True)

#     except Exception as e:
#         raise Exception(f"Error fetching signed PDF: {str(e)}")
        
        
# def save_signed_pdf(pdf_content, file_name):
#     """Save signed PDF content to the media folder."""
#     pdf_path = os.path.join(settings.MEDIA_ROOT, 'signed_pdfs', file_name)
#     os.makedirs(os.path.dirname(pdf_path), exist_ok=True)  # Ensure folder exists

#     with open(pdf_path, 'wb') as pdf_file:
#         pdf_file.write(pdf_content)

#     return pdf_path  # Return the file path for reuse