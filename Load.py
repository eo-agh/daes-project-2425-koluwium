import requests
import pandas as pd
import time
import os
from datetime import datetime
import sqlite3
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import LocalOutlierFactor
import numpy as np


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


def create_stations_table(database_name: str):
    """Tworzy tabelę STATIONS i uzupełnia współrzędne stacji."""
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS STATIONS (
                Station_Id TEXT PRIMARY KEY,
                Station_name TEXT NOT NULL,
                latitude REAL,
                longitude REAL
            )
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO STATIONS (Station_Id, Station_name)
            SELECT DISTINCT Station_Id, Station_Name FROM METEO
        ''')

        coordinates = {
            'Białystok': (53.1325, 23.1688),
            'Bielsko Biała': (49.8225, 19.0469),
            'Chojnice': (53.6957, 17.5566),
            'Częstochowa': (50.8118, 19.1203),
            'Elbląg': (54.1522, 19.4088),
            'Gdańsk': (54.3520, 18.6466),
            'Gorzów': (52.7368, 15.2288),
            'Hel': (54.6081, 18.8008),
            'Jelenia Góra': (50.9044, 15.7194),
            'Kalisz': (51.7611, 18.0910),
            'Kasprowy Wierch': (49.2314, 19.9817),
            'Katowice': (50.2649, 19.0238),
            'Kętrzyn': (54.0766, 21.3755),
            'Kielce': (50.8661, 20.6286),
            'Kłodzko': (50.4344, 16.6619),
            'Koło': (52.2002, 18.6383),
            'Kołobrzeg': (54.1756, 15.5835),
            'Koszalin': (54.1944, 16.1722),
            'Kozienice': (51.5824, 21.5471),
            'Kraków': (50.0647, 19.9450),
            'Krosno': (49.6931, 21.7702),
            'Legnica': (51.2101, 16.1619),
            'Lesko': (49.4701, 22.3293),
            'Leszno': (51.8407, 16.5740),
            'Lębork': (54.5394, 17.7519),
            'Lublin': (51.2465, 22.5684),
            'Łeba': (54.7551, 17.5381),
            'Łódź': (51.7592, 19.4550),
            'Mikołajki': (53.8001, 21.5803),
            'Mława': (53.1122, 20.3831),
            'Nowy Sącz': (49.6216, 20.6971),
            'Olsztyn': (53.7784, 20.4801),
            'Opole': (50.6751, 17.9213),
            'Ostrołęka': (53.0842, 21.5758),
            'Piła': (53.1510, 16.7385),
            'Platforma': (54.5, 18.5),
            'Płock': (52.5468, 19.7064),
            'Poznań': (52.4064, 16.9252),
            'Przemyśl': (49.7842, 22.7672),
            'Racibórz': (50.0915, 18.2199),
            'Resko': (53.7734, 15.4064),
            'Rzeszów': (50.0413, 21.9990),
            'Sandomierz': (50.6820, 21.7480),
            'Siedlce': (52.1676, 22.2900),
            'Słubice': (52.3437, 14.5600),
            'Sulejów': (51.3540, 19.8855),
            'Suwałki': (54.1118, 22.9309),
            'Szczecin': (53.4285, 14.5528),
            'Szczecinek': (53.7070, 16.6994),
            'Śnieżka': (50.7365, 15.7404),
            'Świnoujście': (53.9103, 14.2470),
            'Tarnów': (50.0138, 20.9869),
            'Terespol': (52.0754, 23.6165),
            'Toruń': (53.0138, 18.5984),
            'Ustka': (54.5804, 16.8619),
            'Warszawa': (52.2297, 21.0122),
            'Wieluń': (51.2211, 18.5690),
            'Włodawa': (51.5488, 23.5490),
            'Wrocław': (51.1079, 17.0385),
            'Zakopane': (49.2992, 19.9496),
            'Zamość': (50.7174, 23.2523),
            'Zielona Góra': (51.9356, 15.5064)
        }

        for name, (lat, lon) in coordinates.items():
            cursor.execute('''
                UPDATE STATIONS
                SET latitude = ?, longitude = ?
                WHERE station_name = ?
            ''', (lat, lon, name))

        conn.commit()
        cursor.execute("SELECT * FROM STATIONS")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        conn.close()

    except sqlite3.Error as e:
        print(f"Błąd podczas tworzenia tabeli STATIONS: {e}")


def load_data(df, table_name, conn):
    try:
        if df is None or df.empty:
            print("Brak danych do załadowania.")
            return

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
            cursor.execute(f"INSERT INTO {table_name} SELECT * FROM {table_name}_deduped;")
            cursor.execute(f"DROP TABLE {table_name}_deduped;")

    except Exception as e:
        print(f"ERROR in loading data to the database: {e}")


def create_grid_data_from_latest(conn, cursor, grid_step=0.5):
    cursor.execute("DROP TABLE IF EXISTS Grid_Data;")
    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STATIONS'")
    if cursor.fetchone() is None:
        print("Tabela STATIONS nie istnieje – uruchom create_stations_table().")
        return

    cursor.execute("SELECT MAX(Date) FROM METEO")
    max_date = cursor.fetchone()[0]
    cursor.execute("SELECT MAX(Hour) FROM METEO WHERE Date = ?", (max_date,))
    max_hour = cursor.fetchone()[0]

    query = """
    SELECT 
        METEO.Station_Id, 
        METEO.Station_Name, 
        METEO.Temperature, 
        STATIONS.longitude, 
        STATIONS.latitude
    FROM METEO
    JOIN STATIONS ON METEO.Station_Id = STATIONS.Station_Id
    WHERE METEO.Date = ? AND METEO.Hour = ?
    AND METEO.Temperature IS NOT NULL
    """
    df = pd.read_sql_query(query, conn, params=(max_date, max_hour))

    if df.empty:
        print("Brak danych najnowszych pomiarów.")
        return

    lof = LocalOutlierFactor(n_neighbors=10)
    outlier_flags = lof.fit_predict(df[['Temperature']])
    df_clean = df[outlier_flags == 1].reset_index(drop=True)

    if len(df_clean) < 10:
        print("Za mało punktów po usunięciu outlierów.")
        return

    X_train = df_clean[['longitude', 'latitude']].values
    y_train = df_clean['Temperature'].values

    lon_min, lon_max = X_train[:,0].min(), X_train[:,0].max()
    lat_min, lat_max = X_train[:,1].min(), X_train[:,1].max()

    lon_grid = np.arange(lon_min, lon_max + grid_step, grid_step)
    lat_grid = np.arange(lat_min, lat_max + grid_step, grid_step)
    grid_points = np.array([[lon, lat] for lat in lat_grid for lon in lon_grid])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    temps_pred = model.predict(grid_points)

    df_grid = pd.DataFrame({
        'Longitude': grid_points[:,0],
        'Latitude': grid_points[:,1],
        'Date': max_date,
        'Hour': max_hour,
        'Temperature': temps_pred
    })

    cursor.execute("""
        CREATE TABLE Grid_Data (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Longitude FLOAT,
            Latitude FLOAT,
            Date TEXT,
            Hour INT,
            Temperature FLOAT
        );
    """)
    conn.commit()

    df_grid.to_sql('Grid_Data', conn, if_exists='append', index=False)
    print(f"Grid data are created using random forest.")
