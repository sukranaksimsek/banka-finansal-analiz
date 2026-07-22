# 🏦 Banka Finansal Performans Analizi

BIST'te işlem gören dört büyük banka hissesinin (Garanti BBVA, Akbank, İş Bankası, Yapı Kredi)
zaman içindeki fiyat performansını, volatilitesini ve aralarındaki korelasyonu analiz eden
uçtan uca bir veri analizi projesi.

## 🎯 Amaç

- Python ile finansal veri çekme ve temizleme
- SQL ile ilişkisel veri analizi (window functions, group by)
- Python ile getiri/volatilite hesaplama ve görselleştirme

## 🛠️ Kullanılan Araçlar

- **Python**: pandas, yfinance, matplotlib, seaborn
- **SQL**: SQLite (sqlalchemy üzerinden)
- **Veri Kaynağı**: Yahoo Finance (yfinance)

## 📁 Proje Yapısı
banka-finansal-analiz/
├── data/
│ ├── raw/ # Ham CSV verisi (gitignore'da)
│ └── processed/ # SQLite DB + grafikler
├── notebooks/
│ ├── 01_veri_toplama.py
│ ├── 02_sql_aktarma.py
│ └── 03_gorsellestirme.py
├── sql/
│ └── sorgular.sql # Analiz sorguları
├── requirements.txt
└── README.md
## 🚀 Nasıl Çalıştırılır

```bash
# 1. Sanal ortam oluştur ve kütüphaneleri kur
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Veriyi çek
python notebooks/01_veri_toplama.py

# 3. SQLite veritabanına aktar
python notebooks/02_sql_aktarma.py

# 4. Görselleştirmeleri oluştur
python notebooks/03_gorsellestirme.py
```

## 📝 İlerleme Günlüğü

- [x] Gün 1: Proje iskeleti, README, requirements.txt oluşturuldu
- [x] Gün 2: Veri çekme scripti çalıştırıldı, 6552 satır veri elde edildi
- [ ] Gün 3: SQLite'a aktarma ve SQL sorguları
- [ ] Gün 4: Görselleştirme ve bulgular

## 📊 Bulgular
.
.
.

## 📌 Notlar

- Analiz dönemi: 2020-01-01 → 2026-07-18
- Veri kaynağı ücretsiz olduğu için gecikmeli/eksik veri içerebilir, yatırım tavsiyesi değildir.

## 👤 Yazar

Şükran Akşimşek
[www.linkedin.com/in/sukranaksimsek](https://www.linkedin.com/in/sukranaksimsek)
