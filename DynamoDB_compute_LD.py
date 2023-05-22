import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sound')
    
    if 'id' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing id value in the request'})
        }
    

    response = table.put_item(
        Item={
            'id': event['id']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data stored successfully'})
    }
