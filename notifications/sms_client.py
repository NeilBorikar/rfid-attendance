from twilio.rest import Client
from utils.env_utils import get_required_env


class SMSClient:
    def __init__(self):
        self.account_sid = get_required_env("TWILIO_ACCOUNT_SID")
        self.auth_token = get_required_env("TWILIO_AUTH_TOKEN")
        self.from_number = get_required_env("TWILIO_PHONE_NUMBER")

        self.client = Client(
            self.account_sid,
            self.auth_token
        )

    def send_sms(self, to: str, message: str):
        """
        Send SMS message using Twilio.
        """
        # Ensure 'to' number starts with '+' for international format
        to_number = to if to.startswith("+") else f"+91{to}"  # Assuming India default if no prefix

        try:
            message_instance = self.client.messages.create(
                from_=self.from_number,
                to=to_number,
                body=message
            )
            return {"status": "success", "sid": message_instance.sid}
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            return {"status": "error", "message": str(e)}
