
import boto3
import os

# Get credentials from OS variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Get the service resource
dynamodb = boto3.client('dynamodb', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-west-2')

print('Creating DynamoDB table for Shopping...')

# Create DynamoDB table for shopping items
dynamodb.create_table(
    TableName='shopping',
    KeySchema=[
        {
            'AttributeName': 'order_date',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'customerid_timestamp',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'customerid_timestamp',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'order_date',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

print('DynamoDB table created for Shopping.')
