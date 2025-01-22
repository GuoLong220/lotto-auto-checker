import os
import requests, json

from dotenv import load_dotenv
load_dotenv()

line_bot_access_token = os.getenv('line_bot_access_token')
line_group_id = os.getenv('line_group_id')
def bot(text):
    headers = {'Authorization':f'Bearer {line_bot_access_token}','Content-Type':'application/json'}
    body = {
        'to':line_group_id,
        'messages':[{
                'type': 'text',
                'text': text
            }]
        }

    try:
        req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))
        if req.status_code != 200:
            return req.text
        return True
    except Exception as error:
        return error
