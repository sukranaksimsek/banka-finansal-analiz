-- ============================================================
-- Banka Finansal Performans Analizi - SQL Sorguları
-- Veritabanı: data/processed/banka.db
-- Tablo: banka_fiyatlari
-- ============================================================

-- 1) Her bankanın kaç günlük veri içerdiğini kontrol et
SELECT Banka_Adi, COUNT(*) AS gun_sayisi
FROM banka_fiyatlari
GROUP BY Banka_Adi;

-- 2) Her bankanın genel ortalama kapanış fiyatı
SELECT Banka_Adi, ROUND(AVG(Kapanis), 2) AS ortalama_kapanis
FROM banka_fiyatlari
GROUP BY Banka_Adi
ORDER BY ortalama_kapanis DESC;

-- 3) Aylık ortalama kapanış fiyatı (her banka için)
SELECT
    Banka_Adi,
    strftime('%Y-%m', Tarih) AS ay,
    ROUND(AVG(Kapanis), 2) AS aylik_ortalama
FROM banka_fiyatlari
GROUP BY Banka_Adi, ay
ORDER BY Banka_Adi, ay;

-- 4) En yüksek ve en düşük kapanış fiyatının görüldüğü tarihler
SELECT
    Banka_Adi,
    MAX(Kapanis) AS en_yuksek_kapanis,
    MIN(Kapanis) AS en_dusuk_kapanis
FROM banka_fiyatlari
GROUP BY Banka_Adi;

-- 5) Günlük yüzdesel değişim (window function ile önceki güne göre)
SELECT
    Banka_Adi,
    Tarih,
    Kapanis,
    ROUND(
        (Kapanis - LAG(Kapanis) OVER (PARTITION BY Banka_Adi ORDER BY Tarih))
        / LAG(Kapanis) OVER (PARTITION BY Banka_Adi ORDER BY Tarih) * 100
    , 2) AS gunluk_degisim_yuzde
FROM banka_fiyatlari
ORDER BY Banka_Adi, Tarih;

-- 6) En yüksek ortalama günlük işlem hacmine sahip banka
SELECT Banka_Adi, ROUND(AVG(Hacim), 0) AS ortalama_hacim
FROM banka_fiyatlari
GROUP BY Banka_Adi
ORDER BY ortalama_hacim DESC;

-- 7) Yıllık başlangıç ve bitiş fiyatlarına göre toplam getiri (%)
WITH yillik AS (
    SELECT
        Banka_Adi,
        strftime('%Y', Tarih) AS yil,
        FIRST_VALUE(Kapanis) OVER (
            PARTITION BY Banka_Adi, strftime('%Y', Tarih)
            ORDER BY Tarih
        ) AS yil_ilk_fiyat,
        LAST_VALUE(Kapanis) OVER (
            PARTITION BY Banka_Adi, strftime('%Y', Tarih)
            ORDER BY Tarih
            RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS yil_son_fiyat
    FROM banka_fiyatlari
)
SELECT DISTINCT
    Banka_Adi,
    yil,
    ROUND((yil_son_fiyat - yil_ilk_fiyat) / yil_ilk_fiyat * 100, 2) AS yillik_getiri_yuzde
FROM yillik
ORDER BY Banka_Adi, yil;
