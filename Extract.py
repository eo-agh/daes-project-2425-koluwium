import requests
import pandas as pd
import time
import os


def extract_data(url):
    """ Pobiera dane z API IMGW """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        now = time.localtime()

        df = pd.DataFrame(data)
        
        now = time.localtime()
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', now)} - Data are loaded.")
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR in extracting data: {e}")

    return df
