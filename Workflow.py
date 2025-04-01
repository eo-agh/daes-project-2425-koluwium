import requests
import pandas as pd
import time
import os
from datetime import datetime
import sqlite3
from Load import load_data, create_database
from Extract import extract_data

url = 'https://danepubliczne.imgw.pl/api/data/synop'
database_name = 'data'

conn, cursor = create_database(database_name)


while True:
    df = extract_data(url)
    load_data(df, "METEO", conn)

    time.sleep(1800) 
