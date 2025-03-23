import requests
import pandas as pd
import time
import os
from datetime import datetime

url = 'https://danepubliczne.imgw.pl/api/data/synop'

def fetch_and_save_data():
    """ Pobiera dane z API IMGW i zapisuje je do pliku CSV w odpowiednim folderze """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)

        timestamp_date = datetime.now().strftime("%Y%m%d")
        timestamp_hour = datetime.now().strftime("%H")
        timestamp_hour = int(timestamp_hour)-1
        timestamp_month = datetime.now().strftime("%Y_%m") 

        base_folder = "./dane"
        os.makedirs(base_folder, exist_ok=True)

        month_folder = os.path.join(base_folder, timestamp_month)
        os.makedirs(month_folder, exist_ok=True)

        day_folder = os.path.join(month_folder, timestamp_date)
        os.makedirs(day_folder, exist_ok=True)

        filename = os.path.join(day_folder, f"dane_{timestamp_date}_{timestamp_hour}.csv")

        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"[{timestamp_date} {timestamp_hour}] Dane zapisano do '{filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych: {e}")

# Pobieranie danych co godzinę
while True:
    fetch_and_save_data()
    time.sleep(3600) 
