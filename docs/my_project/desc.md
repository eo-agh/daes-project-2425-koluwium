# 🌦️ Inteligentna Prognoza Pogody oparta na Uczeniu Maszynowym

## 📌 Opis projektu

Projekt ma na celu stworzenie systemu prognozy pogody w czasie rzeczywistym z wykorzystaniem uczenia maszynowego oraz analizy danych historycznych. Model przewiduje warunki atmosferyczne na podstawie zbieranych danych meteorologicznych, takich jak:

- temperatura
- wilgotność względna
- ciśnienie atmosferyczne
- opady
- prędkość i kierunek wiatru

## 🎯 Cel projektu

Głównym celem jest zaprojektowanie oraz wdrożenie kompletnego **data workflow**, obejmującego następujące etapy:

- ⏬ Automatyczne pobieranie danych meteorologicznych z serwisu **IMGW** w interwałach godzinowych i zapisywanie ich do bazy "sqlite"
- 🧹 Przetwarzanie, czyszczenie i przygotowanie danych do analizy i modelowania
- 💾 Zapisanie danych do relacyjnej bazy danych
- 🧠 Wykorzystanie danych do trenowania modeli predykcyjnych (ML/DL)
- 📊 Prezentacja wyników poprzez dashboard, raport lub eksport danych
- ☁️ Możliwość integracji z usługami chmurowymi (np. Azure)

## 🛠️ Technologie i narzędzia

| Etap | Narzędzia |
|------|-----------|
| Pobieranie danych | `requests`, `json` |
| Analiza danych | `pandas`, `numpy` |
| Przechowywanie danych | `SQLite`, `PostgreSQL`, `SQLAlchemy` |
| Modelowanie | `scikit-learn`, `PyTorch` |
| Wizualizacja | `matplotlib`, `seaborn`, `Plotly`, `Dash` |
| Automatyzacja | `cron`, `Airflow` (opcjonalnie) |
| Kontrola wersji | `Git`, `GitHub` |
| Chmura (opcjonalnie) | `Azure` |

## 🔁 Metodyka

Projekt opiera się na podejściu **ETL (Extract, Transform, Load)** oraz wykorzystuje klasyczne techniki przetwarzania danych i modelowania predykcyjnego. Planowane podejścia:

- Automatyzacja pobierania danych (skrypty Python + harmonogram zadań)
- Transformacja i oczyszczanie danych (handling braków danych, normalizacja, standaryzacja)
- Budowa modeli ML/DL do prognozy pogody
- Ewaluacja modeli (RMSE, MAE, accuracy, itp.)
- Wizualizacja predykcji i integracja z bazą danych lub interfejsem użytkownika

## 🚀 Planowane rozszerzenia

- Wykorzystanie prognoz numerycznych jako danych wejściowych (np. GFS, ECMWF)
- Rozbudowany dashboard z interaktywną mapą
- Deployment w chmurze (Server AGH)
- API do udostępniania prognoz ---trochę Sen o Warszawie

## 👨‍💻 Autor
Hałys Filip, Bartosz Staroń, Szymon Trojak

> Projekt realizowany w ramach przedmiotu "Analiza danych w naukach o Ziemi".
