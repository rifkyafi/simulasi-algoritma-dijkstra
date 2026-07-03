# Optimasi Jalur Pengiriman Makanan Siaga Bencana

Program simulasi jaringan darat untuk mencari **rute terpendek** pengiriman logistik bencana menggunakan **Algoritma Dijkstra**. Program ini memodelkan titik-titik lokasi (posko induk, shelter, desa) sebagai simpul graf dan jalur darat sebagai sisi berbobot (menit tempuh).

---

## Fitur

1. **Lihat peta jaringan darat** — menampilkan seluruh titik dan koneksi jalur
2. **Cari rute terpendek (Dijkstra)** — input ID asal & tujuan, output jalur dan total jarak
3. **Tampilkan semua rute dari Posko Induk** — daftar jarak dan jalur ke seluruh lokasi
4. **Simulasi jalur putus (re-routing)** — pengguna memilih jalur yang terputus akibat bencana, sistem menghitung ulang rute alternatif
5. **Urgensi pengiriman** — daftar prioritas lokasi berdasarkan nilai urgensi

---

## Struktur Kode

| Komponen | File | Penjelasan |
|---|---|---|
| `Graph` | `test.py:5-56` | Graf dengan adjacency list; method `tambah_jalur`, `putuskan_jalur`, `dijkstra`, `rute_terpendek` |
| `Titik` | `test.py:59-67` | Simpul dengan atribut `id`, `nama`, `jenis`, `urgensi` |
| `JaringanBencana` | `test.py:70-104` | Pengelola graf dan titik; method `tambah_titik`, `tambah_jalur`, `putuskan_jalur`, `cari_rute`, `semua_rute_dari_posko` |
| `menu()` | `test.py:219-276` | Loop utama CLI 5 menu interaktif |

### Algoritma Dijkstra (baris 23-42)

```
1. Inisialisasi jarak[start] = 0, jarak[node lain] = ∞
2. Masukkan (0, start) ke priority queue (min-heap)
3. Selama pq tidak kosong:
   a. Ambil node dengan jarak terkecil
   b. Jika jarak_sekarang > jarak[node], skip (stale entry)
   c. Untuk setiap tetangga:
      - total = jarak_sekarang + bobot
      - Jika total < jarak[tetangga], perbarui & push ke pq
```

Kompleksitas: **O((V+E) log V)** dengan _binary heap_.

---

## Topologi Jaringan (Default)

```
Posko Induk (1) ──15── Shelter A (2) ──20── Desa C (4) ──8── Desa E (6)
                │                   │                   │
               30                  25                  12
                │                   │                   │
             Shelter B (3) ──10── Desa C (4)    Desa D (5)
                                                    │   │
                                                   18  14
                                                    │   │
                                                 Desa E (6) ──22── Desa F (7)
```

| ID | Nama | Jenis | Urgensi |
|---|---|---|---|
| 1 | Posko Induk | depot | 5 |
| 2 | Shelter A | shelter | 8 |
| 3 | Shelter B | shelter | 7 |
| 4 | Desa C | desa | 9 |
| 5 | Desa D | desa | 6 |
| 6 | Desa E | desa | 10 |
| 7 | Desa F | desa | 4 |

---

## Contoh Input & Output

### Menu 1 — Lihat Peta

```
  Pilih (0-5): 1

=================================================================
  PETA JARINGAN DARAT - POSKO BENCANA
=================================================================
  ID  NAMA           JENIS      URGENSI
  ---------------------------------------------
  1   Posko Induk    depot      5
  2   Shelter A      shelter    8
  3   Shelter B      shelter    7
  4   Desa C         desa       9
  5   Desa D         desa       6
  6   Desa E         desa       10
  7   Desa F         desa       4

  KONEKSI JALUR (bobot = menit tempuh):
    Posko Induk  --(15 menit)--> Shelter A
    Posko Induk  --(30 menit)--> Shelter B
    Shelter A    --(20 menit)--> Desa C
    Shelter A    --(25 menit)--> Desa D
    Shelter B    --(10 menit)--> Desa C
    Desa C       --(12 menit)--> Desa D
    Desa C       --( 8 menit)--> Desa E
    Desa D       --(18 menit)--> Desa E
    Desa D       --(14 menit)--> Desa F
    Desa E       --(22 menit)--> Desa F
```

### Menu 2 — Cari Rute Terpendek

```
  Pilih (0-5): 2

  Daftar titik:
  1. Posko Induk (depot)
  2. Shelter A (shelter)
  3. Shelter B (shelter)
  4. Desa C (desa)
  5. Desa D (desa)
  6. Desa E (desa)
  7. Desa F (desa)
  ID asal: 1
  ID tujuan: 7

-----------------------------------------------------------------
  RUTE TERPENDEK (DIJKSTRA)
  Dari : Posko Induk (ID 1)
  Ke   : Desa F (ID 7)
  Jalur: Posko Induk -> Shelter A -> Desa C -> Desa E -> Desa F
  Jarak: 49 menit
  Simpul: [1, 2, 4, 6, 7]
```

### Menu 3 — Semua Rute dari Posko Induk

```
  Pilih (0-5): 3

=================================================================
  SEMUA RUTE DARI POSKO INDUK (ID 1)
=================================================================
  -> Shelter A    :  15 menit  | Posko Induk -> Shelter A
  -> Shelter B    :  30 menit  | Posko Induk -> Shelter B
  -> Desa C       :  35 menit  | Posko Induk -> Shelter A -> Desa C
  -> Desa D       :  40 menit  | Posko Induk -> Shelter A -> Desa C -> Desa D
  -> Desa E       :  43 menit  | Posko Induk -> Shelter A -> Desa C -> Desa E
  -> Desa F       :  49 menit  | Posko Induk -> Shelter A -> Desa C -> Desa E -> Desa F
```

### Menu 4 — Simulasi Jalur Putus

```
  Pilih (0-5): 4

=================================================================
  SIMULASI JALUR DARAT TERPUTUS
=================================================================
  Jalur yang tersedia untuk diputus:
  1. Posko Induk -- Shelter A (15 menit)
  2. Posko Induk -- Shelter B (30 menit)
  3. Shelter A -- Desa C (20 menit)
  4. Shelter A -- Desa D (25 menit)
  5. Shelter B -- Desa C (10 menit)
  6. Desa C -- Desa D (12 menit)
  7. Desa C -- Desa E (8 menit)
  8. Desa D -- Desa E (18 menit)
  9. Desa D -- Desa F (14 menit)
  10. Desa E -- Desa F (22 menit)

  Pilih nomor jalur yang putus (0 = batal): 1

  [PUTUS] Jalur Posko Induk -- Shelter A terputus akibat bencana!

  DAMPAK PADA RUTE DARI POSKO INDUK:
  -> Shelter A    :  60 menit  | Posko Induk -> Shelter B -> Desa C -> Desa D -> Desa E -> Shelter A
  -> Shelter B    :  30 menit  | Posko Induk -> Shelter B
  -> Desa C       :  40 menit  | Posko Induk -> Shelter B -> Desa C
  -> Desa D       :  52 menit  | Posko Induk -> Shelter B -> Desa C -> Desa D
  -> Desa E       :  60 menit  | Posko Induk -> Shelter B -> Desa C -> Desa E
  -> Desa F       :  74 menit  | Posko Induk -> Shelter B -> Desa C -> Desa D -> Desa F
```

### Menu 5 — Urgensi Pengiriman

```
  Pilih (0-5): 5

=================================================================
  URGENSI PENGIRIMAN MAKANAN
=================================================================
   1. Desa E        Urgensi: 10
   2. Desa C        Urgensi: 9
   3. Shelter A     Urgensi: 8
   4. Shelter B     Urgensi: 7
   5. Desa D        Urgensi: 6
   6. Posko Induk   Urgensi: 5
   7. Desa F        Urgensi: 4

  Semakin tinggi urgensi, semakin prioritas pengiriman.
```

---

## Cara Menjalankan

```bash
python test.py
```

Pastikan Python 3.6+ terinstal. Tidak ada dependensi eksternal (hanya menggunakan `heapq` dan `os` bawaan).

---

## Catatan

- Program berjalan di **CLI interaktif**. Pilih menu dengan memasukkan angka 0–5.
- Bobot jalur dinyatakan dalam **menit tempuh**.
- Saat jalur diputus (menu 4), sistem otomatis menghitung ulang rute dari Posko Induk ke semua titik menggunakan Dijkstra.
- Jika suatu lokasi tidak terjangkau sama sekali, akan muncul pesan **TIDAK TERJANGKAU**.
