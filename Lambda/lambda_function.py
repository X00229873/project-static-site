import json
import helper_file
import escalation_helper

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # For debugging
    
    user_input = event.get('inputTranscript', '').lower()
    intent_name = event['sessionState']['intent']['name']

    message = "I'm sorry, I couldn't understand your request. Please contact support."

    if "yes" in user_input:
        # User says YES
        message = helper_file.send_success_response()
    
    elif "no" in user_input:
        # User says NO
        message = escalation_helper.escalate_to_human()

    elif intent_name == "AccountAccessIntent":
        if "password" in user_input:
            message = (
                "It looks like you forgot your password. You can reset it here:\n"
                "https://pulsepointcare.com/reset-password\n\n"
                "Is your problem resolved? Was the article useful to fix your problem?"
            )
        elif "mfa" in user_input or "two-factor" in user_input or "2fa" in user_input:
            message = (
                "It looks like you're having MFA (Two-Factor Authentication) issues. Troubleshoot it here:\n"
                "https://pulsepointcare.com/mfa-help\n\n"
                "Is your problem resolved? Was the article useful to fix your problem?"
            )
        elif "locked" in user_input or "suspended" in user_input:
            message = (
                "It seems your account is locked or suspended. Recover your account here:\n"
                "https://pulsepointcare.com/account-recovery\n\n"
                "Is your problem resolved? Was the article useful to fix your problem?"
            )
        elif "login" in user_input or "log in" in user_input:
            message = (
                "Having trouble logging in? You can reset your password or troubleshoot MFA here:\n"
                "- Password reset: https://pulsepointcare.com/reset-password\n"
                "- MFA help: https://pulsepointcare.com/mfa-help\n\n"
                "Is your problem resolved? Was the article useful to fix your problem?"
            )
        else:
            message = (
                "You might try resetting your password or troubleshooting your MFA.\n\n"
                "- Reset password: https://pulsepointcare.com/reset-password\n"
                "- MFA troubleshooting: https://pulsepointcare.com/mfa-help\n"
                "- Contact support: https://pulsepointcare.com/contact-support\n\n"
                "Is your problem resolved? Was the article useful to fix your problem?"
            )

    elif intent_name == "NetworkConnectivityIntent":
        message = (
            "It looks like you're having network or VPN issues. Here's what you can try:\n\n"
            "- Restart your router or modem.\n"
            "- Reconnect to Wi-Fi.\n"
            "- Check VPN settings and reconnect.\n\n"
            "If problems continue, see this troubleshooting guide:\n"
            "https://pulsepointcare.com/network-help\n\n"
            "Is your problem resolved? Was the article useful to fix your problem?"
        )

    elif intent_name == "SoftwareInstallationIntent":
        message = (
            "Need to install software?\n\n"
            "- Access the Company Portal app on your computer.\n"
            "- Search for the app you need (like Microsoft Teams, Zoom, etc.).\n"
            "- Click Install.\n\n"
            "If you don't see the app you need, request assistance here:\n"
            "https://pulsepointcare.com/software-request\n\n"
            "Is your problem resolved? Was the article useful to fix your problem?"
        )

    else:
        message = (
            "I'm sorry, I couldn't find a direct solution for your issue.\n\n"
            "- Reset password: https://pulsepointcare.com/reset-password\n"
            "- Troubleshoot MFA: https://pulsepointcare.com/mfa-help\n"
            "- Network help: https://pulsepointcare.com/network-help\n"
            "- Request software: https://pulsepointcare.com/software-request\n"
            "- Contact support: https://pulsepointcare.com/contact-support\n\n"
            "Is your problem resolved? Was the article useful to fix your problem?"
        )

    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }
