from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

class MessageSender:
    def __init__(self):
        # Load Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
        
        # Contact dictionary - you can expand this
        self.contacts = {
            "mom": "+1234567890",    # Replace with actual number
            "dad": "+0987654321",    # Replace with actual number
            "sister": "+1122334455" , # Replace with actual number
            "manager": "+919345410542"  # Replace with actual number
        }
        
        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_message(self, to_number: str, message: str) -> str:
        """
        Send a message using Twilio
        Args:
            to_number (str): The recipient's phone number (format: +1234567890)
            message (str): The message to send
        Returns:
            str: Status message
        """
        try:
            # Send the message
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return f"Message sent successfully! SID: {message.sid}"
        except Exception as e:
            return f"Failed to send message: {str(e)}"
    
    def send_whatsapp(self, name: str, message: str) -> str:
        """
        Send a WhatsApp message to a contact
        Args:
            name (str): Contact name (must be in contacts dictionary)
            message (str): The message to send
        Returns:
            str: Status message
        """
        try:
            # Check if contact exists
            if name.lower() not in self.contacts:
                return f"Contact '{name}' not found in contacts list"
            
            # Get number from contacts
            to_number = f"whatsapp:+919514076681"
            
            # Send the WhatsApp message
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )

            # message = self.client.messages.create(
            #     from_='whatsapp:+14155238886',
            #     content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
            #     content_variables='{"1":"12/1","2":"3pm"}',
            #     to='whatsapp:+919514076681'
            # )
            return f"WhatsApp message sent to {name} successfully! SID: {message.sid}"
        except Exception as e:
            return f"Failed to send WhatsApp message: {str(e)}"
        


        # test 

