import json
import urllib.parse
import boto3
from datetime import datetime

rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
table = dynamodb.Table('VisionMemoriesData')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        print(f"Analyzing image: '{key}' from bucket: '{bucket}'")

        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=10,
            MinConfidence=75
        )
        detected_labels = [label['Name'] for label in response['Labels']]
        print(f"AI Detected: {detected_labels}")

        creative_text = generate_creative_text(detected_labels)

        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table.put_item(
            Item={
                'ImageID': key,
                'UploadTime': upload_time,
                'DetectedObjects': detected_labels,
                'CreativeText': creative_text,
                'Status': 'Analyzed'
            }
        )
        print(f"Successfully saved analysis for {key} to DynamoDB!")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Image {key} analyzed and saved successfully.")
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e


def generate_creative_text(labels):
    try:
        labels_str = ', '.join(labels)
        prompt = f"""You are a marketing copywriter for an e-commerce website.
Based on the following features detected in the image: {labels_str}
Write a short, persuasive product description in Hebrew (2-3 sentences only).
Return only the description, no titles or additional explanations."""

        body = json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "inferenceConfig": {"maxTokens": 200, "temperature": 0.7}
        })

        response = bedrock_client.invoke_model(
            modelId='amazon.nova-lite-v1:0',
            body=body
        )
        result = json.loads(response['body'].read())
        creative_text = result['output']['message']['content'][0]['text']
        print(f"Bedrock generated: {creative_text}")
        return creative_text

    except Exception as e:
        print(f"Bedrock error (non-critical): {str(e)}")
        return "Marketing description coming soon."
