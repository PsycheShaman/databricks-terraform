import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

# Replace with your SQS queue URL
SQS_QUEUE_URL = 'https://sqs.eu-west-1.amazonaws.com/889562587392/raw-listing-bucket-events-queue'

def lambda_handler(event, context):
    for record in event['Records']:
        s3_event = record['eventName']
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        event_time = record['eventTime']
        
        if 'ObjectCreated' in s3_event:
            event_type = 'create'
        elif 'ObjectRemoved' in s3_event:
            event_type = 'delete'
        else:
            event_type = 'unknown'
        
        # Initialize file contents
        file_contents = None
        
        # Get file contents if event is create
        if event_type == 'create':
            try:
                obj = s3.get_object(Bucket=bucket_name, Key=object_key)
                file_contents = obj['Body'].read().decode('utf-8')
            except Exception as e:
                print(f"Error getting object {object_key} from bucket {bucket_name}: {e}")
        
        # Construct the message payload
        message_payload = {
            'bucket_name': bucket_name,
            'object_key': object_key,
            'event_type': event_type,
            'event_time': event_time,
            'file_contents': file_contents
        }
        
        # Send message to SQS
        try:
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message_payload)
            )
            print(f"Message sent to SQS: {message_payload}")
        except Exception as e:
            print(f"Error sending message to SQS: {e}")
        
    return {
        'statusCode': 200,
        'body': json.dumps('Event processed')
    }
