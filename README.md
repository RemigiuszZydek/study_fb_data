# 📊 Football Scraper (Serie A)

Projekt do scrapowania danych meczów Serie A z LiveScore oraz zapisu do bazy danych lub CSV.

---

# 🚀 1. Instalacja środowiska

## 📁 Klon repozytorium

git clone <URL_TWOJEGO_REPO>
cd study_fb_data

---

## 🐍 Tworzenie virtualenv

Windows (PowerShell):
python -m venv venv
venv\Scripts\activate

Mac / Linux:
python3 -m venv venv
source venv/bin/activate

---

# 📦 2. Instalacja zależności

pip install -r requirements.txt

---

# 🧱 3. Baza danych (SQLite)

python main.py

---

# ⚙️ 4. Uruchomienie scrapera

DB mode:
python -m scrapers.serie_a_scraper

CSV mode:
Zmień funkcję na save_match_to_csv()

Generalnie jak ktos chce odpalic scrapper i tylko np do bazy logowac dane albo tylko do csv to zakomentowac jedna funkcje w serie_a_scraper.py

---

# ⚠️ 5. Wymagania

- Chrome zainstalowany
- Selenium (pip install selenium)

---

# 📌 6. Struktura projektu

study_fb_data/
├── db/
├── scrapers/
├── venv/
├── requirements.txt
├── livescore.db
├── main.py
