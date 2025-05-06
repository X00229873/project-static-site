import json
import boto3

ses_client = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))

    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent'].get('slots', {})
    username_slot = slots.get('username', {}).get('value', {}).get('interpretedValue')

    if intent_name == "PasswordResetIntent":
        if username_slot:
            email_address = f"{username_slot}@gmail.com"
            sent = send_email(email_address)
            message = (
                f"A password reset link has been sent to {email_address}."
                if sent else
                "There was an error sending the email. Please contact support."
            )
        else:
            message = "I need your username to proceed. What is your account username?"

        return build_response(intent_name, message)

    return build_response(intent_name, "Sorry, I didn't understand your request.")

def send_email(to_address):
    try:
        ses_client.send_email(
            Source='support@yourdomain.com',  # Replace with verified email in SES
            Destination={'ToAddresses': [to_address]},
            Message={
                'Subject': {'Data': 'Password Reset Instructions'},
                'Body': {
                    'Text': {
                        'Data': (
                            "Hello,\n\n"
                            "Here’s your link to reset your password:\n"
                            "https://pulsepointcare.com/reset-password\n\n"
                            "If this wasn’t requested, you can ignore it.\n\n"
                            "Best,\nTechBuddy Support"
                        )
                    }
                }
            }
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def build_response(intent_name, message):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"name": intent_name, "state": "Fulfilled"}
        },
        "messages": [{"contentType": "PlainText", "content": message}]
    }
