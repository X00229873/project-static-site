import json
import helper_file
import escalation_helper

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # For debugging

    user_input = event.get('inputTranscript', '').lower()
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent'].get('slots', {})

    message = "I'm sorry, I couldn't understand your request. Please contact support."

    if intent_name == "PasswordResetIntent":
        account_slot = slots.get('account', {}).get('value', {}).get('interpretedValue')

        if account_slot:
            helper_file.send_password_reset_email(account_slot)
            message = (
                f"A password reset link has been sent to {account_slot}. "
                "Please check your inbox and spam folder.\n\n"
                "Let me know if this help you solve the problem?"
            )
        else:
            message = (
                "I was expecting an account to send the reset instructions to, but I couldn't find it. "
                "Please try again or contact support at +3530987564324 or email techforce@pulsepoint.com."
            )

    elif intent_name == "AccountAccessIntent":
        if "password" in user_input:
            message = (
                "It looks like you forgot your password. You can reset it here:\n"
                "https://pulsepointbucket.s3.us-east-1.amazonaws.com/SelfServicePortal/index2.html\n\n"
                "Was the provided support useful to fix your problem?"
            )
        elif "mfa" in user_input or "two-factor" in user_input or "2fa" in user_input:
            message = (
                "It looks like you're having MFA (Two-Factor Authentication) issues. Troubleshoot it here:\n"
                "https://pulsepointbucket.s3.us-east-1.amazonaws.com/MFAHelpPage/Index3.html\n\n"
                "Was the provided support useful to fix your problem?"
            )
        elif "locked" in user_input or "suspended" in user_input:
            message = (
                "It seems your account is locked or suspended. Contact support at:\n"
                "+3530987564324 or email techforce@pulsepoint.com.\n\n"
                "Was the provided support useful to fix your problem?"
            )
        elif "login" in user_input or "log in" in user_input:
            message = (
                "Having trouble logging in? You can reset your password or troubleshoot MFA here:\n"
                "- Password reset: https://pulsepointbucket.s3.us-east-1.amazonaws.com/SelfServicePortal/index2.html\n"
                "- MFA help: https://pulsepointbucket.s3.us-east-1.amazonaws.com/MFAHelpPage/Index3.html\n\n"
                "Was the provided support useful to fix your problem?"
            )
        else:
            message = (
                "You might try resetting your password or troubleshooting your MFA.\n\n"
                "- Reset password: https://pulsepointbucket.s3.us-east-1.amazonaws.com/SelfServicePortal/index2.html\n"
                "- MFA troubleshooting: https://pulsepointbucket.s3.us-east-1.amazonaws.com/MFAHelpPage/Index3.html\n"
                "- Contact support: +3530987564324 or email techforce@pulsepoint.com.\n\n"
                "Was the provided support useful to fix your problem?"
            )

    elif intent_name == "NetworkConnectivityIntent":
        message = (
            "It looks like you're having network or VPN issues. Here's what you can try:\n\n"
            "- Restart your router or modem.\n"
            "- Reconnect to Wi-Fi.\n"
            "- Check VPN settings and reconnect.\n\n"
            "If problems continue, see this troubleshooting guide:\n"
            "https://pulsepointbucket.s3.us-east-1.amazonaws.com/NetworkHelpPage/index4.html\n\n"
            "Was the provided support useful to fix your problem?"
        )

    elif intent_name == "SoftwareInstallationIntent":
        message = (
            "Need to install software?\n\n"
            "- Access the Company Portal app on your computer.\n\n"
            "https://pulsepointbucket.s3.us-east-1.amazonaws.com/SoftwarePortal/index5.html\n"
            "- Search for the app you need (like Microsoft Teams, Zoom, etc.).\n"
            "- Click Install.\n\n"
            "Was the provided support useful to fix your problem?"
        )

    elif intent_name == "EscalateIntent":
        message = escalation_helper.escalate_to_human()

    elif intent_name == "SuccessIntent":
        message = "I'm glad to hear that! Let me know if you need help with anything else."

    else:
        message = (
            "I'm sorry, I couldn't find a direct solution for your issue.\n\n"
            "- Reset password: https://pulsepointbucket.s3.us-east-1.amazonaws.com/SelfServicePortal/index2.html\n"
            "- Troubleshoot MFA: https://pulsepointbucket.s3.us-east-1.amazonaws.com/MFAHelpPage/Index3.html\n"
            "- Network help: https://pulsepointbucket.s3.us-east-1.amazonaws.com/NetworkHelpPage/index4.html\n"
            "- Request software: https://pulsepointbucket.s3.us-east-1.amazonaws.com/SoftwarePortal/index5.html\n"
            "- Contact support: +3530987564324 or email techforce@pulsepoint.com.\n\n"
            "Is your problem resolved? Was the article useful to fix your problem?"
        )

    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"name": intent_name, "state": "Fulfilled"}
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }