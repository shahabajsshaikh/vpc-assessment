import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Check if specific resource ID is requested
        resource_id = event.get('queryStringParameters', {}).get('resourceId')
        
        if resource_id:
            # Get specific resource
            response = table.get_item(Key={'resourceId': resource_id})
            item = response.get('Item', {})
            
            if not item:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Resource not found'})
                }
                
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            # Scan for all resources
            response = table.scan()
            items = response.get('Items', [])
            
            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }