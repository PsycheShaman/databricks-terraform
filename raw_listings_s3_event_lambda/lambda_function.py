import json
import boto3
import hashlib
from datetime import datetime

s3 = boto3.client('s3')

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
        
        # Hash the message payload to create a unique filename
        message_hash = hashlib.md5(json.dumps(message_payload).encode()).hexdigest()

        message_payload = {
            'bucket_name': bucket_name,
            'object_key': object_key,
            'event_id': message_hash,
            'event_type': event_type,
            'event_time': event_time,
            'file_contents': file_contents,
        }

        s3_key = f"listings/{message_hash}.json"
        
        # Write message payload to S3
        try:
            s3.put_object(
                Bucket='z-staging',
                Key=s3_key,
                Body=json.dumps(message_payload)
            )
            print(f"Message written to S3: {s3_key}")
        except Exception as e:
            print(f"Error writing message to S3: {e}")
        
    return {
        'statusCode': 200,
        'body': json.dumps('Event processed')
    }
