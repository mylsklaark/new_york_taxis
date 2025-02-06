FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY src/data_ingestion/ingest_tables.py /app/ingest_tables.py

ENTRYPOINT [ "python",  "ingest_tables.py" ]