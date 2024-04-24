#!/usr/bin/env bash

until printf "" 2>>/dev/null >>/dev/tcp/cassandra/9042; do
    sleep 5;
    echo "Waiting for cassandra...";
done

echo "Creating keyspace and table..."
cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS sales_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS sales_ks.sales_table 
      (
        uuid uuid primary key,
        pos_id int, 
        pos_name text,
        article text, 
        quantity float,
        unit_price float, 
        total float, 
        sale_type text,
        payment_mode text,
        sale_time text,
        year int,
        month int,
        week_number int,
        day_of_week text
      );"


# cqlsh cassandra -u cassandra -p cassandra -e "select * from sales_ks.sales_table;"