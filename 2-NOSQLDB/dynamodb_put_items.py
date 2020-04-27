
import boto3
import os
from decimal import Decimal

# Get credentials from OS variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Get the service resource
dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-west-2')

# Items data to put on DynamoDB
customers_data = {
    235416: {"firstname": "Bob", "lastname": "Adams", "zipcode": 33948},
    455416: {"firstname": "Amy", "lastname": "Smith", "zipcode": 38948},
    545416: {"firstname": "Rob", "lastname": "Bennet", "zipcode": 41948}
}

items_data = {
    "sk46573": {"title": "USB", "price": Decimal('10.2')},
    "sk54373": {"title": "Mouse", "price": Decimal('12.23')},
    "sk75373": {"title": "Monitor", "price": Decimal('199.99')}
}

items_bought_data = [
    {"customerid": 235416, "order_date": "2020-04-25", "customerid_timestamp": "235416_2020-04-25 09:42:34", "itemsku": "sk46573", "quantity_bought": 2, "total_price": Decimal('20.4')},
    {"customerid": 455416, "order_date": "2020-04-25", "customerid_timestamp": "455416_2020-04-25 10:42:34", "itemsku": "sk54373", "quantity_bought": 3, "total_price": Decimal('36.69')},
    {"customerid": 545416, "order_date": "2020-04-25", "customerid_timestamp": "545416_2020-04-25 11:42:34", "itemsku": "sk75373", "quantity_bought": 1, "total_price": Decimal('199.99')},
    {"customerid": 235416, "order_date": "2020-04-25", "customerid_timestamp": "235416_2020-04-25 12:42:34", "itemsku": "sk46573", "quantity_bought": 5, "total_price": Decimal('51.0')},
    {"customerid": 545416, "order_date": "2020-04-25", "customerid_timestamp": "545416_2020-04-25 13:42:34", "itemsku": "sk54373", "quantity_bought": 2, "total_price": Decimal('24.46')}
]


# Putting data on DynamoDB
print("Start putting data into shopping table...")

shopping_table = dynamodb.Table('shopping')
with shopping_table.batch_writer() as batch:
    for item_bought in items_bought_data:
        item_bought['customer'] = customers_data[item_bought['customerid']]
        item_bought['item'] = items_data[item_bought['itemsku']]
        batch.put_item(Item=item_bought)

print("Finished putting data into shopping table.")