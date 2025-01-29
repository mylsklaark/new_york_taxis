## PostgreSQL database and pgAdmin web interface

A project to set up a PostgreSQL database and pgAdmin web interface using Docker Compose. It includes two services:
 
 - a PostgreSQL container (pgdatabase) with persistent data storage
 - a pgAdmin container (pgadmin) for managing and visualizing the database. 
 
 The containers are connected via a custom network (pg-network), allowing for interaction between the database and the admin interface. Data persistence is ensured with Docker volumes, enabling data to survive container restarts.


You can use pgcli to interact with the PostgreSQL database:
'''bash
pgcli -h localhost -p 5432 -u postgres -d ny_taxi
