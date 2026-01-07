import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'visitor-counter'))

def lambda_handler(event, context):
    try:
        # Get current count
        response = table.get_item(Key={'id': 'visitor-count'})
        
        if 'Item' in response:
            count = int(response['Item']['count']) + 1
        else:
            count = 1
        
        # Update count
        table.put_item(Item={'id': 'visitor-count', 'count': count})
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'count': count})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }