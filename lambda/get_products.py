import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisionMemoriesData')

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])
    items.sort(key=lambda x: x.get('UploadTime', ''), reverse=True)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items, default=str, ensure_ascii=False)
    }
