"""
01_veri_toplama.py
-------------------
BIST'te işlem gören banka hisselerinin günlük fiyat verilerini
Yahoo Finance üzerinden çeker ve data/raw klasörüne CSV olarak kaydeder.

Not: Bu betiği kendi bilgisayarında çalıştırman gerekiyor
(bu ortamda dış ağ erişimi kısıtlı).
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

# Analiz edilecek bankalar (BIST kodları)
BANKALAR = {
    "GARAN.IS": "Garanti BBVA",
    "AKBNK.IS": "Akbank",
    "ISCTR.IS": "İş Bankası (C)",
    "YKBNK.IS": "Yapı Kredi",
}

BASLANGIC_TARIHI = "2020-01-01"
BITIS_TARIHI = "2026-07-18"

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def veri_cek():
    tum_veriler = []

    for kod, isim in BANKALAR.items():
        print(f"Çekiliyor: {isim} ({kod}) ...")
        df = yf.download(kod, start=BASLANGIC_TARIHI, end=BITIS_TARIHI, progress=False)

        if df.empty:
            print(f"  UYARI: {kod} için veri bulunamadı, atlanıyor.")
            continue

        # Çoklu index (MultiColumn) durumunu düzelt
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df["Banka_Kodu"] = kod
        df["Banka_Adi"] = isim
        tum_veriler.append(df)

    if not tum_veriler:
        raise RuntimeError("Hiçbir banka için veri çekilemedi.")

    birlesik = pd.concat(tum_veriler, ignore_index=True)

    # Kolon isimlerini sadeleştir
    birlesik = birlesik.rename(columns={
        "Date": "Tarih",
        "Open": "Acilis",
        "High": "Yuksek",
        "Low": "Dusuk",
        "Close": "Kapanis",
        "Adj Close": "Duzeltilmis_Kapanis",
        "Volume": "Hacim",
    })

    cikti_yolu = OUTPUT_DIR / "banka_fiyatlari.csv"
    birlesik.to_csv(cikti_yolu, index=False)
    print(f"\nToplam {len(birlesik)} satır kaydedildi -> {cikti_yolu}")

    return birlesik


if __name__ == "__main__":
    veri_cek()
