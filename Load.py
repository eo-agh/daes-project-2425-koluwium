import requests
import pandas as pd
import time
import os
from datetime import datetime
import sqlite3


def create_database(name: str):
    conn = sqlite3.connect(f'{name}.db')
    cursor = conn.cursor()
    cursor.execute('''

        CREATE TABLE IF NOT EXISTS METEO (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Station_Id INT,
            Station_Name VARCHAR(50),
            Date TEXT,
            Hour INT,
            Temperature FLOAT,
            Wind_Speed FLOAT,
            Wind_Direction INT, 
            Relative_Humidity FLOAT, 
            Precipitation_Total FLOAT, 
            Pressure FLOAT
        )

    ''')

    conn.commit()

    print(f"Database {name} is created.")

    return conn, cursor
    

def load_data(df, table_name, conn):
    try:
        df = df.rename(columns={
            'id_stacji': 'Station_Id',
            'stacja': 'Station_Name',
            'data_pomiaru': 'Date',
            'godzina_pomiaru': 'Hour',
            'temperatura': 'Temperature',
            'predkosc_wiatru': 'Wind_Speed',
            'kierunek_wiatru': 'Wind_Direction',
            'wilgotnosc_wzgledna': 'Relative_Humidity',
            'suma_opadu': 'Precipitation_Total',
            'cisnienie': 'Pressure'
        })

        df.to_sql(table_name, conn, if_exists='append', index=False)

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TEMP TABLE {table_name}_deduped AS
                SELECT * FROM {table_name}
                WHERE rowid IN (
                    SELECT MIN(rowid)
                    FROM {table_name}
                    GROUP BY Station_Id, Date, Hour
                );
            """)

            cursor.execute(f"DELETE FROM {table_name};")

            cursor.execute(f"""
                INSERT INTO {table_name}
                SELECT * FROM {table_name}_deduped;
            """)

            cursor.execute(f"DROP TABLE {table_name}_deduped;")

    except Exception as e:
        print(f"ERROR in loading data to the database: {e}")

