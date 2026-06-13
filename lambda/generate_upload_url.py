import json
import boto3
import uuid

s3_client = boto3.client('s3')
BUCKET = 'smart-vision-memories-platform-2026'

def lambda_handler(event, context):
    body = json.loads(event.get('body') or '{}')
    file_name = body.get('fileName', 'product.jpg')
    key = f"{uuid.uuid4().hex[:8]}_{file_name}"

    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET, 'Key': key, 'ContentType': 'image/jpeg'},
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'uploadURL': upload_url, 'key': key})
    }
