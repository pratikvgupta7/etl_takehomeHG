import os
import pandas as pd
import psycopg2

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

file_path = 'data/inbound/customer_churn_data.csv'

conn = psycopg2.connect(
    host = DB_HOST,
    database = DB_NAME,
    user = DB_USER,
    password = DB_PASSWORD
)

df = pd.read_csv(file_path)
df.columns = [c.lower() for c in df.columns]

cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
                   INSERT INTO raw.customer_churn_raw
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                   """,
                   tuple(row)
                   )

conn.commit()
cursor.close()
conn.close()

print("Data ingestion completed successfully.")

