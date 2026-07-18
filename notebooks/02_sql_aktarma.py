"""
02_sql_aktarma.py
------------------
data/raw/banka_fiyatlari.csv dosyasını okuyup bir SQLite veritabanına
(data/processed/banka.db) yükler. Böylece SQL sorgularını bu DB üzerinde
çalıştırabilirsin.
"""

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_YOLU = BASE_DIR / "data" / "raw" / "banka_fiyatlari.csv"
DB_YOLU = BASE_DIR / "data" / "processed" / "banka.db"

DB_YOLU.parent.mkdir(parents=True, exist_ok=True)


def sql_e_aktar():
    df = pd.read_csv(CSV_YOLU, parse_dates=["Tarih"])

    engine = create_engine(f"sqlite:///{DB_YOLU}")
    df.to_sql("banka_fiyatlari", engine, if_exists="replace", index=False)

    print(f"{len(df)} satır '{DB_YOLU}' veritabanına 'banka_fiyatlari' tablosu olarak yazıldı.")


if __name__ == "__main__":
    sql_e_aktar()
