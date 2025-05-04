import os
import json
import urllib.request

def escalate_to_human():
    slack_webhook_url = os.environ['Techforce']
    
    payload = {
        "text": "Support needed!\n<@U08PX8SCZ8B> please assist in the last thread.",
        # You can also use a group like <@support_team_id>
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(slack_webhook_url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return "A human support agent has been notified in Slack!"
            else:
                return "There was a problem notifying the support team."
    except Exception as e:
        print(f"Error sending Slack webhook: {e}")
        return "Escalation failed. Please contact support manually."
