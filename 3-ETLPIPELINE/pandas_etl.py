#!/usr/bin/env python3

"""
Script that extracts and process information by using pandas dataframe from mysql and dynamo Shopping DBs to store it into Redshift DWH
"""

import boto3
from boto3.dynamodb.conditions import Key
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
import pandas as pd
import decimal
import json
import os
import re

# Get datetime to process (on real scenario this script will be running daily by initializing this date as current date)
datetime_to_process = datetime(year=2020, month=4, day=25, hour=0, minute=0, second=0, microsecond=0)
mysql_dt_format = "%Y-%m-%d %H:%M:%S"
dynamo_dt_format = "%Y-%m-%d"

# Get credentials from OS variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DBNAME = os.getenv('MYSQL_DBNAME')
REDSHIFT_USERNAME = os.getenv('REDSHIFT_USERNAME')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_DBNAME = os.getenv('REDSHIFT_DBNAME')

# Query for MySQL DB
MYSQL_SHOPPING_QUERY = f"""
SELECT 
  CONVERT(ib.item_id, char) as itemid_sku, 
  ib.quantity_bought as quantity, 
  ib.total_price,
  ib.order_timestamp,
  c.address,
  i.name as item_name
FROM items_bought ib 
JOIN customer c 
ON c.user_id = ib.user_id
JOIN items i 
ON i.item_id = ib.item_id
WHERE ib.order_timestamp BETWEEN '{datetime_to_process.strftime(mysql_dt_format)}' 
AND '{(datetime_to_process + timedelta(days=1)).strftime(mysql_dt_format)}'
"""

# DynamoDB variables to query
DYNAMO_TABLE = 'shopping'
DYNAMO_CONDITIONALS = Key('order_date').eq(datetime_to_process.strftime(dynamo_dt_format))

# Redshift target table to store the data
REDSHIFT_TABLE = 'global_sells'

# USD to MXN rate
MXN_TO_USD_RATE = 0.04


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_mysql_query_df(query):
    """
    Get mysql query results as pandas dataframe

    :param query: Query to be runt and retrieved as pandas dataframe
    :return: Pandas dataframe of query results
    """
    db_connection_str = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DBNAME}'
    db_connection = create_engine(db_connection_str)
    return pd.read_sql(query, con=db_connection)


def get_dynamo_query_df(table_name, conditionals):
    """
    Get dynamo query results as pandas dataframe

    :param table_name: Table name to query
    :param conditionals: Key conditionals of the query
    :return: Pandas dataframe of query results
    """
    # Get the service resource for DynamoDB
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2')
    # Retrieve DynamoDB table resource
    table = dynamodb.Table(table_name)
    # Retrieve query result as normalized pandas dataframe
    return pd.json_normalize(json.loads(json.dumps(table.query(KeyConditionExpression=conditionals)['Items'], cls=DecimalEncoder)))


def send_dataframe_to_redshift(table_name, dataframe):
    """
    Send pandas dataframe to redshift table

    :param table_name: Target table name to store the data
    :param dataframe: Dataframe to send to redshift
    :return:
    """
    conn = create_engine(f'redshift://{REDSHIFT_USERNAME}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DBNAME}')
    dataframe.to_sql(table_name, conn, index=False, if_exists='replace')


# Get mysql and dynamo data as pandas dataframe
mysql_df = get_mysql_query_df(MYSQL_SHOPPING_QUERY)
dynamo_df = get_dynamo_query_df(DYNAMO_TABLE, DYNAMO_CONDITIONALS)

# Processing mysql_df to have clean data for the DWH (extract zip code from address and convert totaL_price from MXN to USD)
mysql_df['zip_code'] = mysql_df['address'].apply(lambda address: re.search("CP (\d+)", address).group(1))
mysql_df['total_price'] = mysql_df['total_price'].apply(lambda price: price * MXN_TO_USD_RATE)
del mysql_df['address']

# Processing dynamo_df to have clean data for the DWH (extract timestamp and rename columns for DWH column names)
dynamo_df['order_timestamp'] = dynamo_df['customerid_timestamp'].apply(lambda x: x.split('_')[1])

dynamo_df.rename(columns={
    'itemsku': 'itemid_sku',
    'quantity_bought': 'quantity',
    'item.title': 'item_name',
    'customer.zipcode': 'zip_code'},
    inplace=True)

for column in ['customerid_timestamp', 'order_date', 'customerid', 'customer.firstname', 'customer.lastname', 'item.price']:
    del dynamo_df[column]

# Making a union of clean mysql_df and clean dynamo_df data for DWH
redshift_df = pd.concat([mysql_df, dynamo_df])
print("Data to send to redshift")
print(redshift_df)

# Uncomment the following line when having valid redshift connection variables to send the data to the DWH
# send_dataframe_to_redshift(REDSHIFT_TABLE, redshift_df)

print(f"ETL script successfully completed for date {datetime_to_process.strftime(dynamo_dt_format)}.")
