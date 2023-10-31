-- Membuat tabel "mobil" untuk menyimpan data mobil
CREATE TABLE mobil (
    id SERIAL PRIMARY KEY,
    nama_mobil VARCHAR(255),
    harga DECIMAL,
    volume_langkah_cc DECIMAL,
    tangki_bensin DECIMAL,
    daya_maksimum_kW DECIMAL,
    torsi_maksimum_Nm DECIMAL
);

-- Menyisipkan data mobil ke dalam tabel "mobil"
INSERT INTO mobil (nama_mobil, harga, volume_langkah_cc, tangki_bensin, daya_maksimum_kW, torsi_maksimum_Nm)
VALUES
    ('Toyota Camry', 214200000, 1462, 60, 178, 221),
    ('Honda Civic', 219900000, 1000, 46, 126, 148),
    ('Ford Mustang', 432670000, 1569, 61, 310, 440),
    ('Chevrolet Silverado', 421400000, 2125, 98, 285, 413),
    ('BMW 3 Series', 222550000, 1248, 59, 181, 270),
    ('Mercedes-Benz C-Class', 323050000, 1486, 66, 154, 250),
    ('Audi A4', 419960000, 2125, 58, 170, 237),
    ('Nissan Rogue', 627500000, 4486, 55, 128, 154),
    ('Hyundai Elantra', 535750000, 5509, 53, 182, 264),
    ('Volkswagen Golf', 527175000, 4155, 50, 160, 292);

-- Menampilkan data dari tabel "mobil"
SELECT * FROM mobil;
