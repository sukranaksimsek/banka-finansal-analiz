"""
03_gorsellestirme.py
---------------------
data/processed/banka.db içindeki veriyi okuyup
temel finansal görselleştirmeleri üretir ve data/processed
klasörüne PNG olarak kaydeder.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_YOLU = BASE_DIR / "data" / "processed" / "banka.db"
CIKTI_DIR = BASE_DIR / "data" / "processed"

sns.set_theme(style="whitegrid")


def veriyi_oku():
    engine = create_engine(f"sqlite:///{DB_YOLU}")
    df = pd.read_sql("SELECT * FROM banka_fiyatlari", engine, parse_dates=["Tarih"])
    return df


def fiyat_trend_grafigi(df):
    plt.figure(figsize=(12, 6))
    for banka in df["Banka_Adi"].unique():
        alt = df[df["Banka_Adi"] == banka]
        plt.plot(alt["Tarih"], alt["Kapanis"], label=banka)

    plt.title("Banka Hisselerinin Zaman İçindeki Kapanış Fiyatları")
    plt.xlabel("Tarih")
    plt.ylabel("Kapanış Fiyatı (TL)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(CIKTI_DIR / "fiyat_trend.png", dpi=150)
    plt.close()


def gunluk_getiri_hesapla(df):
    df = df.sort_values(["Banka_Adi", "Tarih"]).copy()
    df["Gunluk_Getiri"] = df.groupby("Banka_Adi")["Kapanis"].pct_change()
    return df


def volatilite_karsilastirma(df):
    volatilite = (
        df.groupby("Banka_Adi")["Gunluk_Getiri"]
        .std()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    volatilite.plot(kind="bar", color="steelblue")
    plt.title("Bankalar Arası Günlük Getiri Volatilitesi (Risk)")
    plt.ylabel("Standart Sapma")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(CIKTI_DIR / "volatilite_karsilastirma.png", dpi=150)
    plt.close()

    return volatilite


def korelasyon_isi_haritasi(df):
    pivot = df.pivot(index="Tarih", columns="Banka_Adi", values="Kapanis")
    korelasyon = pivot.pct_change().corr()

    plt.figure(figsize=(7, 6))
    sns.heatmap(korelasyon, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Bankalar Arası Getiri Korelasyonu")
    plt.tight_layout()
    plt.savefig(CIKTI_DIR / "korelasyon_isi_haritasi.png", dpi=150)
    plt.close()


def calistir():
    df = veriyi_oku()
    df = gunluk_getiri_hesapla(df)

    fiyat_trend_grafigi(df)
    volatilite = volatilite_karsilastirma(df)
    korelasyon_isi_haritasi(df)

    print("Grafikler data/processed/ klasörüne kaydedildi:")
    print(" - fiyat_trend.png")
    print(" - volatilite_karsilastirma.png")
    print(" - korelasyon_isi_haritasi.png")
    print("\nVolatilite sıralaması:")
    print(volatilite)


if __name__ == "__main__":
    calistir()
