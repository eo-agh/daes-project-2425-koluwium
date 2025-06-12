import requests
import pandas as pd
import time
import os
from datetime import datetime
import sqlite3
from Load import load_data, create_database, create_grid_data_from_latest
from Extract import extract_data

url = 'https://danepubliczne.imgw.pl/api/data/synop'
database_name = 'data'

def main_loop():
    conn, cursor = create_database(database_name)
    
    while True:
        try:
            print(f"[{datetime.now()}] Start extracting data...")
            df = extract_data(url)

            print(f"[{datetime.now()}] Loading data into database...")
            load_data(df, "METEO", conn)

            print(f"[{datetime.now()}] Creating grid data...")
            create_grid_data_from_latest(conn, cursor, grid_step=0.5)

            print(f"[{datetime.now()}] Sleeping for 30 minutes...\n")
            time.sleep(1800)

        except KeyboardInterrupt:
            print("Zatrzymano ręcznie.")
            break
        except Exception as e:
            print(f"Błąd: {e}")
            print("Ponowna próba za 5 minut.")
            time.sleep(300)

if __name__ == "__main__":
    main_loop()
