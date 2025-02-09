FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY src/data_ingestion/ingest_data_edit.py /app/ingest_data_edit.py

ENTRYPOINT [ "python",  "ingest_data_edit.py" ]