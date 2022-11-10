"""Mailer API for the toEaseShifts application.

    This module manages the sending of e-mails through
    [Sendinblue](https://www.sendinblue.com/), namely to send the schedule of each
    worker for a given month. It can be used to send e-mails tho any users, and with
    any possible content, so as to keep versatility.

    **IMPORTANT**
    To use it, first create an account in Sendinblue. Then you can request an API key
    from them. When you have the key, you will create a .env file, in the same folder
    as this module. In the .env file, write EMAIL_API_KEY="Insert your API key here".
    Without this, the service will not work.

    Typical usage example:

    to = [{"email": "example@example.com", "name": "John Doe"}, ...]
    subject = "A really awesome email"
    content = "<html><body><h1>This is a sample email </h1></body></html>"
    attachments = None

    send_email(to, subject, content, attachments)
"""

from typing import List, TypedDict
from sib_api_v3_sdk.rest import ApiException
import sib_api_v3_sdk
import environ

SENDER = {"name": "toEaseShifts", "email": "toEaseShifts@meic.com"}
RECIPIENT = TypedDict("Recipient", {"email": str, "name": str})
ATTACHMENT = TypedDict("Attachment", {"url": str, "name": str})

env = environ.Env()
environ.Env.read_env()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = env("EMAIL_API_KEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


def send_email(
    recipients: List[RECIPIENT],
    subject: str,
    content: str,
    attachments: List[ATTACHMENT],
) -> None:
    """
    Sends an e-mail through the Sendinblue API, logging any exception that might occur.

    Args:
        recipients: A list of the e-mail receivers
        subject: Subject of the e-mail
        content: Body of the e-mail, as html
        attachments: A list of all the attachments to send with the e-mail
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=recipients,
        html_content=content,
        sender=SENDER,
        subject=subject,
        attachment=attachments,
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as exception:
        print(f"Exception when calling SMTPApi->send_transac_email: {exception}\n")
