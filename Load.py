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
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    except requests.exceptions.RequestException as e:
        print(f"ERROR in loading data to the database: {e}")