import sqlite3

def fetch_all_data_from_db(database_name: str):
    """Pobiera wszystkie dane z tabeli METEO"""
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM METEO")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        conn.close()

    except sqlite3.Error as e:
        print(f"Błąd podczas pobierania danych z bazy: {e}")

def delete_meteo_table(database_name: str):
    """Usuwa tabelę METEO z bazy danych"""
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS METEO")
        conn.commit()

        print("Tabela METEO została usunięta.")

        conn.close()

    except sqlite3.Error as e:
        print(f"Błąd podczas usuwania tabeli z bazy: {e}")





database_name = 'data.db'
fetch_all_data_from_db(database_name)
