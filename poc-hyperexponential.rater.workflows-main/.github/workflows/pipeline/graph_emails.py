#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Graph Emails
#' Author: Mark Fleet
#' Date: 12/02/2025
#' Description: Handles sending emails using MS Graph
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests
import json
import msal
import os

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
user_upn = os.environ.get("EMAIL_UPN")
client_id = os.environ.get("EMAIL_AZURE_AD_CLIENTID")
client_secret = os.environ.get("EMAIL_AZURE_AD_CLIENTSECRET")
tenant_id = os.environ.get("EMAIL_AZURE_AD_TENANTID")
recipient_email_list = os.environ.get("EMAIL_TO")
cc_email_list = os.environ.get("EMAIL_CC")
subject = os.environ.get("EMAIL_SUBJECT")
message_body = os.environ.get("EMAIL_BODY")

def main():

    # Format inputs
    recipient_email_list_formatted = []
    for e in json.loads(recipient_email_list):
        recipient_email_list_formatted.append({'emailAddress': {'Address': e}})

    cc_email_list_formatted = []
    if cc_email_list is not None:
        for e in json.loads(cc_email_list):
            cc_email_list_formatted.append({'emailAddress': {'Address': e}})

    message_body_formatted = message_body.encode().decode('utf-8').strip('\"')
    message_body_formatted = message_body.replace("\n", "<br>")

    # Send email
    send_email(recipient_email_list_formatted, cc_email_list_formatted, subject, message_body_formatted)


def send_email(recipient_email_list, cc_email_list, subject, message_body):

    graph_url = f"https://graph.microsoft.com/v1.0/users/{user_upn}/sendMail"

    # Create a confidential client application
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )

    # Get an access token
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    access_token = result.get("access_token")

    # Create the email message
    email_message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": message_body,
            },
            "toRecipients": recipient_email_list,
            "ccRecipients": cc_email_list,
        },
        "saveToSentItems":"true"
    }

    # Convert the message to JSON format
    email_data = json.dumps(email_message)

    # Send the email
    response = requests.post(
        graph_url,
        headers={
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            'User-Agent': 'My User Agent 1.0',
        },
        data=email_data,
    )

    # Check the response status code
    if response.status_code != 202:
        raise Exception(f"Failed to send email. Status code: {response.status_code}. Error: {response.text}")

if __name__ == "__main__":
    main()