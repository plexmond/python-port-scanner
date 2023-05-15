#
import requests
from config import Config

# mail functionality, based on mailgun
def send_mail(to_email, subject, content):
    return requests.post(
        f"https://api.mailgun.net/v3/{Config.MAILGUN_DOMAIN_NAME}/messages",
        auth=("api", Config.MAILGUN_API_KEY),
        data={"from": Config.FROM_EMAIL,
              "to": [to_email],
              "subject": subject,
              "html": content})


