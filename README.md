# shopping-etl

Shopping ETL to make a data pipeline to extract data from SQL and No SQL DBs into a DWH.

## Repository Setup

This repo has four directories:

- 1-SQLDB: Contains the SQL file to create and populate MySQL DB Tables.
- 2-NOSQLDB: Contains the scripts to create and populate DynamoDB Table.
- 3-ETLPIPELINE: Contains the ETL scripts to store data into the DWH from MySQL and DynamoDB Tables.
- 4-DWH: Contains the SQL file to create the DWH Table.

## MYSQL DB

The MySQL DB contains three tables to store the shopping data which are the following:

- customer: Store the customer personal data (user_id, first_name, last_name, rfc, phone_number, curp and address).
- items: Store the items data that are shipped (item_id, name, price).
- items_bought: Store the records that user bought from the items (it is the intermediary table from the many to many relation from customer and items tables).

## DynamoDB

DynamoDB contains only a single table that store the shopping data, the table is named 'shopping' and contains the following attributes:

- order_date: It contains the date that the item was bought from an userid and it is the PRIMARY KEY of the table.
- customerid_timestamp: It contains both userid and timestamp separated by '_' and it is the SORT KEY of the table.
- itemsku: SKU of the item that was bought.
- quantity_bought: Quantity of items bought.
- total_price: Total price calculated by quantity_bought * item price.
- item: Item object which contains as sub attributes the item data (title that is the name of the item and the price).
- customer: Customer object which contains as sub attributes the customer data (firstname, lastname and zipcode).

## DATAWAREHOUSE

Redshift is the DWH Management Service for this drill. The Shopping DWH only contains a single table named global_sells and will store the historical information for shopping data that is on both MySQL and DynamoDB Databases.

## ETL Scripts

For this drill it was made two options of ETL scripts which are the following:

- pandas_etl.py: This script makes the ETL process by using Pandas Dataframes.
- spark_etl.py: This script makes the ETL process by using Spark Transformation by using pyspark.

To run successfully the ETL scripts it is needed to install the python libraries that are located on requirements.txt file, to install those just run the following command:

`pip install -r ./requirements.txt`

## OS Environment Variables

To run successfully the ETL scripts it is needed to setup the following OS Environment Variables:

- AWS_ACCESS_KEY: AWS IAM User's Access Key to connect to DynamoDB and Redshift.
- AWS_SECRET_KEY: AWS IAM User's Secret Access Key to connect to DynamoDB and Redshift.
- MYSQL_USERNAME: MySQL username to connect to the database.
- MYSQL_PASSWORD: MySQL password to connect to the database.
- MYSQL_HOST: MySQL host to connect to the database.
- MYSQL_DBNAME: MySQL database name to connect.

Also the following OS Environment Variables are optionals (by default the ETL scripts do not send the data to Redshift since the line is commented):

- REDSHIFT_USERNAME: Redshift username to connect to the Data Warehouse.
- REDSHIFT_PASSWORD: Redshift password to connect to the Data Warehouse.
- REDSHIFT_PORT: Redshift port to connect to the Data Warehouse.
- REDSHIFT_HOST: Redshift hostname to connect to the Data Warehouse.
- REDSHIFT_DBNAME: Redshift database name to connect to the Data Warehouse.


