import requests
import pandas as pd
import time


def extract_data(url):
    """Pobiera dane z API IMGW i zwraca jako DataFrame"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        now = time.localtime()
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', now)} - Dane zostały pobrane ({len(df)} rekordów).")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych z API: {e}")
        return None
