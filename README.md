## PostgreSQL Database and pgAdmin Web Interface

This project sets up a **PostgreSQL database** and a **pgAdmin web interface** using **Docker Compose**. It consists of two main services:

- **PostgreSQL Container (`pgdatabase`)**: A container running PostgreSQL with persistent data storage.
- **pgAdmin Container (`pgadmin`)**: A web interface for managing and visualizing the PostgreSQL database.

The containers are connected via a custom network (`pg-network`), allowing them to communicate with each other. **Data persistence** is ensured by Docker volumes, so the data will survive container restarts.

---

### How to Interact with the Database

You can use **pgcli** to interact with the PostgreSQL database. To connect, run the following command:

```bash
pgcli -h localhost -p 5432 -u postgres -d ny_taxi
```

### Project Folder Structure

The project is organized as follows:

```plaintext
.
├── data                                # Data files and related resources
│   ├── ny_taxi_postgres_data          # Folder for PostgreSQL data
│   └── yellow_tripdata_2021-01.csv    # Data file for yellow taxi trips
├── docker                              # Docker-related files for container setup
│   ├── Dockerfile                     # Dockerfile to build custom images
│   └── docker-compose.yaml            # Docker Compose configuration
├── requirements.txt                   # Python dependencies for the project
├── README.md                          # Project documentation
└── src                                 # Source code for the project
    ├── data_ingestion                 # Scripts for ingesting data into PostgreSQL
    ├── pipelines                      # Pipeline automation scripts
    └── services                       # Backend services (API, workers, etc.)
