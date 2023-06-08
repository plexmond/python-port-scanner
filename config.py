# contains mailgun credentials
import os

class Config:
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
    MAILGUN_DOMAIN_NAME = os.getenv('MAILGUN_DOMAIN_NAME', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', '')



