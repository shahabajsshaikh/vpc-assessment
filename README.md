# vpc-assessment
API based VPC Creation.
# AWS VPC Management API

A serverless API for creating VPCs with subnets and retrieving their information.

## Features

- Create VPCs with multiple subnets via API
- Store and retrieve VPC configuration
- Cognito-based authentication
- Fully serverless architecture

## Prerequisites

- AWS CLI configured with admin permissions
- SAM CLI installed
- Python 3.9

## Deployment

1. Clone this repository
2. Run deployment script:
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh


aws cognito-idp sign-up --client-id <UserPoolClientId> --username test@example.com --password Passw0rd!

aws cognito-idp admin-confirm-sign-up --user-pool-id <UserPoolId> --username test@example.

aws cognito-idp initiate-auth --client-id <UserPoolClientId> --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME=test@example.com,PASSWORD=Passw0rd!

curl -X POST <ApiUrl>/vpc \
  -H "Authorization: Bearer <IdToken>" \
  -H "Content-Type: application/json" \
  -d '{
    "cidr_block": "10.0.0.0/16",
    "subnets": [
      {"cidr_block": "10.0.1.0/24", "availability_zone": "us-east-1a"},
      {"cidr_block": "10.0.2.0/24", "availability_zone": "us-east-1b"}
    ]
  }'

curl -X GET <ApiUrl>/vpc \
  -H "Authorization: Bearer <IdToken>"

# Or get specific resource

curl -X GET "<ApiUrl>/vpc?resourceId=<resourceId>" \
  -H "Authorization: Bearer <IdToken>"