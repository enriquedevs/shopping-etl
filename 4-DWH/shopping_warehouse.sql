
-- on shopping warehouse will be the global_sells table that keep records from both SQL and NoSQL DBs after being processed by the ETL Pipeline

CREATE TABLE global_sells (
  itemid_sku varchar(20),
  order_timestamp timestamp,
  quantity int,
  total_price float,
  item_name varchar(100),
  zip_code int
);