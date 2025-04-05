import boto3
import uuid
import json
from datetime import datetime

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body'])
        cidr_block = body.get('cidr_block', '10.0.0.0/16')
        subnet_configs = body.get('subnets', [])
        
        # Create VPC
        vpc_response = ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = vpc_response['Vpc']['VpcId']
        
        # Wait for VPC to be available
        ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])
        
        # Create subnets
        subnets = []
        for config in subnet_configs:
            subnet_response = ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=config['cidr_block'],
                AvailabilityZone=config['availability_zone']
            )
            subnets.append({
                'SubnetId': subnet_response['Subnet']['SubnetId'],
                'CidrBlock': config['cidr_block'],
                'AvailabilityZone': config['availability_zone']
            })
        
        # Store resources in DynamoDB
        resource_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        table.put_item(Item={
            'resourceId': resource_id,
            'vpcId': vpc_id,
            'cidrBlock': cidr_block,
            'subnets': subnets,
            'createdAt': timestamp,
            'status': 'CREATED'
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'VPC and subnets created successfully',
                'resourceId': resource_id,
                'vpcId': vpc_id,
                'subnets': subnets
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }