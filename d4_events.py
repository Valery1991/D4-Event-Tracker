import requests
import time
import json
from datetime import datetime

WEBHOOK_URL = YOUR_WEBHOOK_URL # Replace this with your own discord server's webhook
PAYLOAD_DATA = {
    'content': '',
    'embeds': []
}
last_message_id = None

def fetch_and_send_data():
    try:
        response = requests.get('https://d4armory.io/api/events/recent')
        if response.status_code == 200:
            data = response.json()
            send_to_discord(data)
        else:
            print(f'Request failed with status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

def send_to_discord(data):
    global last_message_id
    global PAYLOAD_DATA
    payload = {
        'content': 'Hello everyone. Here is the current info on D4 events. \n\n**This post is updated automatically!**',
        'embeds': []
    }

    for event_type, event_data in data.items():
        embed = {
            'title': event_type.capitalize(),
            'fields': [],
            'color': '10031634',
            'image': {
                'url': ''
            }
        }
        
        if event_type != 'whispers':
            timestamp = event_data['timestamp']
            formatted_timestamp = f"<t:{timestamp}:R>"
            seconds_passed = datetime.now().timestamp() - datetime.fromtimestamp(timestamp).timestamp()

            if event_type == 'boss':
                if seconds_passed > 0:
                    expected_timestamp = f"<t:{timestamp + 21600}:f>"
                    field = {
                        'name': event_data['nextExpectedName'] if 'nextExpectedName' in event_data else '',
                        'value': f"Next expected spawn: {expected_timestamp}\nLast seen: {formatted_timestamp} in **{event_data['zone']}**",
                        'inline': False
                    }
                else:
                    field = {
                        'name': event_data['name'] if 'name' in event_data else '',
                        'value': f"Next spawn: {formatted_timestamp}\nZone: {event_data['territory']}, **{event_data['zone']}**",
                        'inline': False
                    }
            elif event_type == 'helltide':
                if seconds_passed > 3600:
                    formatted_timestamp = f"<t:{timestamp + 8100}:R>"
                    field = {
                        'name': event_data['name'] if 'name' in event_data else '',
                        'value': f"Next event: {formatted_timestamp}\n\n Helltides are active for 1 hour",
                        'inline': False
                    }
                else:
                    end_timestamp = f"<t:{timestamp + 3600}:R>"
                    embed['image']['url'] = 'https://i.imgur.com/N8jNkrp.jpg'
                    field = {
                        'name': event_data['name'] if 'name' in event_data else '',
                        'value': f"🔥 HELLTIDE CURRENTLY ACTIVE! 🔥\nActive since: {formatted_timestamp}\nEvent ends: {end_timestamp}",
                        'inline': False
                    }
            else:
                if seconds_passed > 0:
                    expected_event = f"<t:{timestamp + 1800}:R>"
                    field = {
                        'name': event_data['name'] if 'name' in event_data else '',
                        'value': f"Started: {formatted_timestamp}\nZone: {event_data['territory']}, **{event_data['zone']}**\nExpected next event: {expected_event}",
                        'inline': False
                    }
                else:
                    field = {
                        'name': event_data['name'] if 'name' in event_data else '',
                        'value': f"Time: {formatted_timestamp}\nZone: {event_data['territory']}, **{event_data['zone']}**",
                        'inline': False
                    }
            embed['fields'].append(field)
            payload['embeds'].append(embed)

    headers = {'Content-Type': 'application/json'}
    print(payload)

    if last_message_id:
        url = f"MESSAGE_ID_HERE" # Replace this with the message ID of the initial event message so it can overwrite it without creating a new message.
        response = requests.patch(url, data=json.dumps(payload), headers=headers)
    else:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

        print(response)

        if response.status_code == 200 or response.status_code == 204:
            if last_message_id == None:
                message_data = response.json()
                last_message_id = message_data['id']
                PAYLOAD_DATA = payload
                return last_message_id, PAYLOAD_DATA
            else:
                print(f'Failed to send/edit message on Discord with status code: {response.status_code}')

if __name__ == '__main__':
    while True:
        fetch_and_send_data()
        time.sleep(300) # Check every 5 minutes
