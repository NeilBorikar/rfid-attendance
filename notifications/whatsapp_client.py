from twilio.rest import Client

from utils.env_utils import get_required_env
from utils.phone_utils import normalize_whatsapp_number


class WhatsAppClient:
    def __init__(self):
        self.account_sid = get_required_env("TWILIO_ACCOUNT_SID")
        self.auth_token = get_required_env("TWILIO_AUTH_TOKEN")
        self.from_number = get_required_env("TWILIO_WHATSAPP_FROM")

        self.client = Client(
            self.account_sid,
            self.auth_token
        )

    def send_message(self, to: str, message: str):
        """
        Send WhatsApp message using Twilio.
        """
        to_number = normalize_whatsapp_number(to)

        self.client.messages.create(
            from_=self.from_number,
            to=to_number,
            body=message
        )
