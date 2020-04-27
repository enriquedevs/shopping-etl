
import boto3
import os

# Get credentials from OS variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Get the service resource
dynamodb = boto3.client('dynamodb', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-west-2')

print('Creating tables...')

# Create DynamoDB tables
dynamodb.create_table(
    TableName='customers',
    KeySchema=[
        {
            'AttributeName': 'firstname',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'lastname',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'firstname',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'lastname',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

dynamodb.create_table(
    TableName='items',
    KeySchema=[
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'price',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'price',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

dynamodb.create_table(
    TableName='items_bought',
    KeySchema=[
        {
            'AttributeName': 'userid',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'order_timestamp',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'userid',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'order_timestamp',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 2,
        'WriteCapacityUnits': 2
    }
)

print('Tables Created.')
