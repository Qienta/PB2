import json
import os
import boto3
import wave

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,AudioMessage,AudioSendMessage,ImageMessage
)

#connect to Line 
line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])

#connect to other service
s3 = boto3.client('s3')
s3_bucket_name = os.environ['S3_BUCKET_NAME']
reGion = os.environ['REGION_NAME']
dynamodb = boto3.resource('dynamodb',region_name=reGion)
table = dynamodb.Table('source')

#getting audio duration
# def get_audio_duration(file_path):
#     with wave.open(file_path, 'rb') as wav_file:
#         frames = wav_file.getnframes()
#         rate = wav_file.getframerate()
        
#     duration = float(frames) / float(rate)
#     return duration

def lambda_handler(event, context):
    
    #store event body and header in var for get content
    body = event['body']
    signature = event['headers']['x-line-signature']

    msg = json.loads(event['body'])
    #msg = event['body']
    message_id = msg['events'][0]['message']['id']
    
    #checking message type
    if msg['events'][0]['message']['type'] == "audio":
        
        message_content = line_bot_api.get_message_content(message_id)
        file_name = f'{message_id}.wav'
        ld_file_path = f'/tmp/{message_id}.wav'

        #write content to S3
        with open(ld_file_path, 'wb' ) as f:
            for chunk in message_content.iter_content():
                f.write(chunk)
            f.close()
        s3.upload_file(ld_file_path,s3_bucket_name,file_name)
       
        #computing audio file in dummy model
        
        #download file from S3
        #s3.download_file(s3_bucket_name, file_name, '/tmp/downloaded.wav')
        #get_audio_duration('/tmp/downloaded.wav')
        
        #calcualate duration
        duration = float(msg['events'][0]['message']['duration'])/1000 
        comp_result = "error"
        
        if duration > 3 :
            comp_result = 'ripe'
            
            line_bot_api.reply_message(
                msg['events'][0]['replyToken'],
                TextSendMessage(text="ทุเรียนสุก")
            )
            
        else:
            comp_result = 'raw'
            
            line_bot_api.reply_message(
                msg['events'][0]['replyToken'],
                TextSendMessage(text="ทุเรียนดิบ")
            )

        obj_endpoint = 'https://'+str(s3_bucket_name)+'.'+str(reGion)+'.amazonaws.com/'+str(file_name)
        
        #upload result to dynamoDB
        response = table.put_item(
            Item={
                'linkendpointobject': obj_endpoint,
                'result' : str(comp_result)
            }
        )
        
    elif msg['events'][0]['message']['type'] == "text":
        line_bot_api.reply_message(
            msg['events'][0]['replyToken'],
            TextSendMessage(text="คุณส่งข้อความ\n โปรดส่งไฟล์เสียงทุเรียน")
        )
        
    elif msg['events'][0]['message']['type'] == "sticker":
        line_bot_api.reply_message(
            msg['events'][0]['replyToken'],
            TextSendMessage(text="คุณส่งสติ๊กเกอร์\n โปรดส่งไฟล์เสียงทุเรียน")
        )
    
    else:
        
        line_bot_api.reply_message(
            msg['events'][0]['replyToken'],
            TextSendMessage(text="คุณส่งอะไรมาจ๊ะเนี่ย\n โปรดส่งไฟล์เสียงทุเรียน")
        )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    }
