import json
import os
import boto3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage
)

line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])

s3 = boto3.client('s3')
s3_bucket_name = os.environ['S3_BUCKET_NAME']


def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        object_size = record['s3']['object']['size']
        
        if s3_bucket_name == bucket_name and object_size > 0:
            line_bot_api.broadcast(TextSendMessage(text="ตรวจพบไฟล์เสียงที่ถูกเพิ่มเข้ามาใน S3"))
            
    return {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    