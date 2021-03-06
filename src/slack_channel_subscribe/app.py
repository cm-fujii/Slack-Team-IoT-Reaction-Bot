import json
import logging
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SLACK_APP_TOKEN_KEY = os.environ['SLACK_APP_TOKEN_KEY']

SLACK_REACTION_NAMES = [
    'kumamon',
    'team_iot',
    'iot_colorful'
]

ssm = boto3.client('ssm')

def lambda_handler(event: dict, context: dict):
    logger.info(event['body'])

    body = json.loads(event['body'])

    if is_reaction_message(body) is False:
        return

    token = get_token()

    for name in SLACK_REACTION_NAMES:
        reaction_slack(body, token, name)

    return {
        'statusCode': 200,
    }

def is_reaction_message(body: dict) -> bool:
    return '熊膳' in body['event']['text']

def get_token() -> str:
    res = ssm.get_parameter(
        Name=SLACK_APP_TOKEN_KEY,
        WithDecryption=True
    )
    return res['Parameter']['Value']

def reaction_slack(body: dict, token: str, name: str) -> None:
    channel = body['event']['channel']
    timestamp = body['event']['event_ts']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    url = 'https://slack.com/api/reactions.add'
    
    data = {
        'channel': channel,
        'name': name,
        'timestamp': timestamp
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except requests.exceptions.RequestException as e:
        logger.error(e)
    else:
        logger.info(response.status_code)
        logger.info(response.text)