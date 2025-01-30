## PostgreSQL Database, pgAdmin Web Interface, and Data Ingestion

This project sets up a **PostgreSQL database**, a **pgAdmin web interface**, and a **data ingestion pipeline** using **Docker**. It consists of three main containers:

- **PostgreSQL Container (`ny_taxi_postgres`)**: A container running PostgreSQL 13, hosting the `ny_taxi` database. This container is responsible for storing the data (e.g., yellow taxi trips) ingested into the database. It listens on port `5432` and has persistent storage configured via Docker volumes, ensuring data is not lost during container restarts.
  
- **pgAdmin Container (`pgadmin`)**: A container running **pgAdmin 4**, a web-based interface for managing and visualizing the PostgreSQL database. The pgAdmin UI is accessible through port `8080` on the host machine, where you can connect to and manage the `ny_taxi_postgres` database. It is connected to the same custom network (`pg-network`) to enable easy communication with the PostgreSQL container.

- **Data Ingestion Container (`taxi_ingest:v001`)**: A custom container designed to ingest large amounts of yellow taxi trip data into the PostgreSQL database. It connects to the `ny_taxi_postgres` container to upload data (e.g., from a CSV or compressed file). The ingestion process happens in chunks, using libraries like `pandas` and `SQLAlchemy` for efficient data handling. This container is also connected to the `pg-network` for easy communication with the PostgreSQL container.

### Container Networking
The containers are connected via a custom Docker network (`pg-network`), enabling them to communicate securely within the same network. This ensures that the ingestion container can connect to the PostgreSQL container and that pgAdmin can access the PostgreSQL database as well.

### Data Persistence
The PostgreSQL container is configured with persistent storage, so the database data survives container restarts. This is achieved using Docker volumes to ensure that the database contents are retained.

### Services Folder
The services folder is included in this repository for convenience. It does not contain sensitive credentials.

---

### Project Folder Structure

The project is organized as follows:

```plaintext
.
├── data                                # Data files and related resources
│   ├── ny_taxi_postgres_data          # Folder for PostgreSQL data
│   └── yellow_tripdata_2021-01.csv    # Data file for yellow taxi trips
├── src                                 # Source code for the project
│   ├── data_ingestion                 # Scripts for ingesting data into PostgreSQL
│   ├── pipelines                      # Pipeline automation scripts
│   └── services                       # Backend services (API, workers, etc.)
├── docker                              # Docker-related files for container setup
│   ├── Dockerfile                     # Dockerfile to build custom images
│   └── docker-compose.yaml            # Docker Compose configuration
├── requirements.txt                   # Python dependencies for the project
├── README.md                          # Project documentation

