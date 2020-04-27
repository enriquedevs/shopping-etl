-- create tables DDLs sentences for shopping sql database

CREATE TABLE IF NOT EXISTS customer (
  user_id int NOT NULL PRIMARY KEY,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  phone_number varchar(15),
  curp varchar(18),
  rfc varchar(13),
  address varchar(255)
);

CREATE TABLE IF NOT EXISTS items (
  item_id int NOT NULL PRIMARY KEY,
  name varchar(100) NOT NULL,
  price float NOT NULL COMMENT 'price in MXN currency'
);

CREATE TABLE IF NOT EXISTS items_bought (
  order_number int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id int,
  item_id int,
  quantity_bought int NOT NULL,
  total_price float NOT NULL,
  order_timestamp timestamp NOT NULL,
  CONSTRAINT fk_userid FOREIGN KEY (user_id) REFERENCES customer(user_id),
  CONSTRAINT fk_itemid FOREIGN KEY (item_id) REFERENCES items(item_id)
);


-- insert into DMLs sentences for shopping sql data

INSERT INTO customer (user_id, first_name, last_name, phone_number, curp, rfc, address) VALUES
(745630, 'ENRIQUE', 'ROSALES', '+5217222407923', 'GARE920606HNTRSN00', 'GARE920606470', 'TEJALPA 64, COL. SANTA ELENA, SAN MATEO ATENCO, CP 52105, MEXICO, MEXICO'),
(845610, 'JAVIER', 'FLORES', '+5215522407913', 'FLRE920606HNTRSN00', 'FLRE920606470', 'PARQUE DE HIGUERAS 24, COL. FORESTA, METEPEC, CP 52143, MEXICO, MEXICO'),
(885610, 'MARIO', 'ARRIAGA', '+5213112407913', 'MARE920606HNTRSN00', 'MARE920606470', 'FLUVIAL 123, COL. FLUVIAL VALLARTA, PUERTO VALLARTA, CP 22143, JALISCO, MEXICO'),
(924620, 'EDUARDO', 'DOMINGO', '+5213322407913', 'REDO920606HNTRSN00', 'REDO920606470', 'EL QUELELE 32, COL. AMAPA, BAHIA DE BANDERAS, CP 32105, NAYARIT, MEXICO');

INSERT INTO items (item_id, name, price) VALUES
(234123, 'IPAD', 29999.99),
(746298, 'MACBOOK PRO', 49999.99),
(893847, 'GALAXY TAB', 11499.00),
(983783, 'IPHONE SE', 14899.99),
(993847, 'HUAWEI P30 PRO', 20999.00);

INSERT INTO items_bought (user_id, item_id, quantity_bought, total_price, order_timestamp) VALUES
(745630, 234123, 2, 59999.98, '2020-04-25 04:00:00'),
(845610, 746298, 1, 49999.99, '2020-04-25 05:00:00'),
(885610, 893847, 3, 34497.00, '2020-04-25 06:00:00'),
(924620, 983783, 5, 74499.95, '2020-04-25 07:00:00'),
(745630, 993847, 1, 20999.00, '2020-04-25 08:00:00'),
(845610, 893847, 1, 11499.00, '2020-04-25 09:00:00'),
(924620, 993847, 1, 20999.00, '2020-04-25 10:00:00');
