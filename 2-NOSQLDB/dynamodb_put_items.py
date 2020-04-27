
import boto3
import os
from decimal import Decimal

# Get credentials from OS variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Get the service resource
dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-west-2')

# Items data to put on DynamoDB
customers_data = [
    {"firstname": "Bob", "lastname": "Adams", "userid": 235416, "zipcode": 33948},
    {"firstname": "Amy", "lastname": "Smith", "userid": 455416, "zipcode": 38948},
    {"firstname": "Rob", "lastname": "Bennet", "userid": 545416, "zipcode": 41948}
]

items_data = [
    {"title": "USB", "price": Decimal('10.2'), "itemsku": "sk46573"},
    {"title": "Mouse", "price": Decimal('12.23'), "itemsku": "sk54373"},
    {"title": "Monitor", "price": Decimal('199.99'), "itemsku": "sk75373"}
]

items_bought_data = [
    {"userid": 235416, "order_timestamp": "2020-04-25T09:42:34Z", "itemsku": "sk46573", "quantity_bought": 2, "total_price": Decimal('20.4')},
    {"userid": 455416, "order_timestamp": "2020-04-25T10:42:34Z", "itemsku": "sk54373", "quantity_bought": 3, "total_price": Decimal('36.69')},
    {"userid": 545416, "order_timestamp": "2020-04-25T11:42:34Z", "itemsku": "sk75373", "quantity_bought": 1, "total_price": Decimal('199.99')},
    {"userid": 235416, "order_timestamp": "2020-04-25T12:42:34Z", "itemsku": "sk46573", "quantity_bought": 5, "total_price": Decimal('51.0')},
    {"userid": 545416, "order_timestamp": "2020-04-25T13:42:34Z", "itemsku": "sk54373", "quantity_bought": 2, "total_price": Decimal('24.46')}
]


# Putting customers on DynamoDB
print("Start putting customer items")

customer_table = dynamodb.Table('customers')
with customer_table.batch_writer() as batch:
    for customer in customers_data:
        batch.put_item(Item=customer)

print("Finished putting customer items")


# Putting items data on DynamoDB
print("Start putting items data")

items_table = dynamodb.Table('items')
with items_table.batch_writer() as batch:
    for item in items_data:
        batch.put_item(Item=item)

print("Finished putting items data")


# Putting items_bought data on DynamoDB
print("Start putting items_bought data")

itemsbought_table = dynamodb.Table('items_bought')
with itemsbought_table.batch_writer() as batch:
    for item_bought in items_bought_data:
        batch.put_item(Item=item_bought)

print("Finished putting items_bought data")