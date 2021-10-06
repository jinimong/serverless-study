import json
import boto3
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    user_id = event.get('user_id')
    conference_type = event.get('type')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    
    if user_id == "*":
        response = table.scan()
    else:
        q = Key('user_id').eq(user_id)
        if conference_type:
            q &= Key('type').eq(conference_type)
        
        response = table.query(
            KeyConditionExpression=q
        )
    
    return {
        'statusCode': 200,
        'items': response['Items'],
        'event': event,
    }
