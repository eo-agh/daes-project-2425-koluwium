import sqlite3

query = "SELECT * FROM stations"
database_name = 'data.db'

def fetch_all_data_from_db(database_name: str, query: str):
    """Pobiera wszystkie dane z tabeli METEO"""
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        conn.close()

    except sqlite3.Error as e:
        print(f"Błąd podczas pobierania danych z bazy: {e}")



fetch_all_data_from_db(database_name, query)
