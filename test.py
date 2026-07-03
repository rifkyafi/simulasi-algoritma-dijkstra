import heapq
import os


class Graph:
    def __init__(self):
        self.adj = {}

    def tambah_jalur(self, u, v, weight):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))

    def putuskan_jalur(self, u, v):
        if u in self.adj:
            self.adj[u] = [(n, w) for n, w in self.adj[u] if n != v]
        if v in self.adj:
            self.adj[v] = [(n, w) for n, w in self.adj[v] if n != u]

    def dijkstra(self, start):
        if start not in self.adj:
            return {}, {}
        jarak = {node: float('inf') for node in self.adj}
        sebelumnya = {node: None for node in self.adj}
        jarak[start] = 0
        pq = [(0, start)]

        while pq:
            jarak_sekarang, node_sekarang = heapq.heappop(pq)
            if jarak_sekarang > jarak[node_sekarang]:
                continue
            for tetangga, bobot in self.adj.get(node_sekarang, []):
                total = jarak_sekarang + bobot
                if total < jarak[tetangga]:
                    jarak[tetangga] = total
                    sebelumnya[tetangga] = node_sekarang
                    heapq.heappush(pq, (total, tetangga))

        return jarak, sebelumnya

    def rute_terpendek(self, start, end):
        if start not in self.adj or end not in self.adj:
            return None, float('inf')
        jarak, sebelumnya = self.dijkstra(start)
        if jarak[end] == float('inf'):
            return None, float('inf')
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = sebelumnya[curr]
        path.reverse()
        return path, jarak[end]


class Titik:
    def __init__(self, id_titik, nama, jenis, urgensi):
        self.id = id_titik
        self.nama = nama
        self.jenis = jenis
        self.urgensi = urgensi

    def __str__(self):
        return f"#{self.id:02d} | {self.nama:<12} | {self.jenis:<8} | Urgensi: {self.urgensi}"


class JaringanBencana:
    def __init__(self):
        self.graph = Graph()
        self.titik = {}
        self.id_counter = 1

    def tambah_titik(self, nama, jenis, urgensi):
        t = Titik(self.id_counter, nama, jenis, urgensi)
        self.titik[self.id_counter] = t
        self.id_counter += 1
        return t

    def tambah_jalur(self, u, v, weight):
        self.graph.tambah_jalur(u, v, weight)

    def putuskan_jalur(self, u, v):
        self.graph.putuskan_jalur(u, v)

    def cari_rute(self, id_dari, id_ke):
        if id_dari not in self.titik or id_ke not in self.titik:
            return None, None, float('inf')
        path_ids, total = self.graph.rute_terpendek(id_dari, id_ke)
        if path_ids is None:
            return None, None, float('inf')
        path_nama = [self.titik[pid].nama for pid in path_ids]
        return path_ids, path_nama, total

    def semua_rute_dari_posko(self, id_posko):
        hasil = []
        for tid in sorted(self.titik):
            if tid == id_posko:
                continue
            _, nama, jarak = self.cari_rute(id_posko, tid)
            hasil.append((tid, self.titik[tid].nama, jarak, nama))
        return hasil


def buat_skenario():
    j = JaringanBencana()
    j.tambah_titik("Posko Induk", "depot", 5)
    j.tambah_titik("Shelter A", "shelter", 8)
    j.tambah_titik("Shelter B", "shelter", 7)
    j.tambah_titik("Desa C", "desa", 9)
    j.tambah_titik("Desa D", "desa", 6)
    j.tambah_titik("Desa E", "desa", 10)
    j.tambah_titik("Desa F", "desa", 4)
    j.tambah_jalur(1, 2, 15)
    j.tambah_jalur(1, 3, 30)
    j.tambah_jalur(2, 4, 20)
    j.tambah_jalur(3, 4, 10)
    j.tambah_jalur(2, 5, 25)
    j.tambah_jalur(4, 5, 12)
    j.tambah_jalur(4, 6, 8)
    j.tambah_jalur(5, 6, 18)
    j.tambah_jalur(5, 7, 14)
    j.tambah_jalur(6, 7, 22)
    return j


def tampil_peta(jaringan):
    print("\n" + "=" * 65)
    print("  PETA JARINGAN DARAT - POSKO BENCANA")
    print("=" * 65)
    print(f"  {'ID':<3} {'NAMA':<14} {'JENIS':<10} {'URGENSI':<8}")
    print("  " + "-" * 45)
    for tid in sorted(jaringan.titik):
        t = jaringan.titik[tid]
        print(f"  {tid:<3} {t.nama:<14} {t.jenis:<10} {t.urgensi:<8}")
    print("\n  KONEKSI JALUR (bobot = menit tempuh):")
    done = set()
    for u in sorted(jaringan.graph.adj):
        for v, w in jaringan.graph.adj[u]:
            key = tuple(sorted((u, v)))
            if key not in done:
                done.add(key)
                print(f"    {jaringan.titik[u].nama:<12} --({w:2d} menit)--> {jaringan.titik[v].nama}")
    print()


def tampil_rute(jaringan, id_dari, id_ke):
    print("\n" + "-" * 65)
    path_ids, path_nama, jarak = jaringan.cari_rute(id_dari, id_ke)
    if path_ids is None:
        print(f"  TIDAK ADA RUTE dari {jaringan.titik[id_dari].nama} ke {jaringan.titik[id_ke].nama}!")
        return
    print(f"  RUTE TERPENDEK (DIJKSTRA)")
    print(f"  Dari : {jaringan.titik[id_dari].nama} (ID {id_dari})")
    print(f"  Ke   : {jaringan.titik[id_ke].nama} (ID {id_ke})")
    print(f"  Jalur: {' -> '.join(path_nama)}")
    print(f"  Jarak: {jarak} menit")
    print(f"  Simpul: {path_ids}")
    print()


def tampil_semua_rute(jaringan):
    print("\n" + "=" * 65)
    print("  SEMUA RUTE DARI POSKO INDUK (ID 1)")
    print("=" * 65)
    hasil = jaringan.semua_rute_dari_posko(1)
    for tid, nama, jarak, path_nama in hasil:
        if jarak == float('inf'):
            print(f"  -> {nama:<12} : TIDAK TERJANGKAU")
        else:
            print(f"  -> {nama:<12} : {jarak:3d} menit  | {' -> '.join(path_nama)}")
    print()


def simulasi_jalur_putus(jaringan):
    print("\n" + "=" * 65)
    print("  SIMULASI JALUR DARAT TERPUTUS")
    print("=" * 65)
    print("  Jalur yang tersedia untuk diputus:")
    done = set()
    daftar = []
    no = 1
    for u in sorted(jaringan.graph.adj):
        for v, w in sorted(jaringan.graph.adj[u], key=lambda x: x[0]):
            key = tuple(sorted((u, v)))
            if key not in done:
                done.add(key)
                nama1 = jaringan.titik[u].nama
                nama2 = jaringan.titik[v].nama
                print(f"  {no}. {nama1} -- {nama2} ({w} menit)")
                daftar.append((u, v))
                no += 1
    if no == 1:
        print("  (tidak ada jalur)")
        return
    pilih = input("\n  Pilih nomor jalur yang putus (0 = batal): ").strip()
    if not pilih.isdigit():
        return
    pilih = int(pilih)
    if pilih < 1 or pilih > len(daftar):
        return
    u, v = daftar[pilih - 1]
    nama1 = jaringan.titik[u].nama
    nama2 = jaringan.titik[v].nama
    print(f"\n  [PUTUS] Jalur {nama1} -- {nama2} terputus akibat bencana!")
    jaringan.putuskan_jalur(u, v)
    print("\n  DAMPAK PADA RUTE DARI POSKO INDUK:")
    hasil = jaringan.semua_rute_dari_posko(1)
    for tid, nama, jarak, path_nama in hasil:
        if jarak == float('inf'):
            print(f"  -> {nama:<12} : TIDAK TERJANGKAU (jalur alternatif habis)")
        else:
            print(f"  -> {nama:<12} : {jarak:3d} menit  | {' -> '.join(path_nama)}")
    print()


def menu():
    jaringan = buat_skenario()
    while True:
        print("\n" + "=" * 65)
        print("  OPTIMASI JALUR PENGIRIMAN MAKANAN SIAGA BENCANA")
        print("  Algoritma Dijkstra pada Graf Jaringan Darat")
        print("=" * 65)
        print("  1. Lihat peta jaringan darat")
        print("  2. Cari rute terpendek (Dijkstra)")
        print("  3. Tampilkan semua rute dari Posko Induk")
        print("  4. Simulasi jalur putus (re-routing)")
        print("  5. Urgensi pengiriman ke seluruh lokasi")
        print("  0. Keluar")
        print("-" * 65)
        pilihan = input("  Pilih (0-5): ").strip()

        if pilihan == "1":
            tampil_peta(jaringan)

        elif pilihan == "2":
            print("\n  Daftar titik:")
            for tid in sorted(jaringan.titik):
                print(f"  {tid}. {jaringan.titik[tid].nama} ({jaringan.titik[tid].jenis})")
            a = input("  ID asal: ").strip()
            b = input("  ID tujuan: ").strip()
            if a.isdigit() and b.isdigit():
                id_a, id_b = int(a), int(b)
                if id_a in jaringan.titik and id_b in jaringan.titik:
                    tampil_rute(jaringan, id_a, id_b)
                else:
                    print("  ID tidak valid!")
            else:
                print("  Masukkan angka!")

        elif pilihan == "3":
            tampil_semua_rute(jaringan)

        elif pilihan == "4":
            simulasi_jalur_putus(jaringan)

        elif pilihan == "5":
            print("\n" + "=" * 65)
            print("  URGENSI PENGIRIMAN MAKANAN")
            print("=" * 65)
            urut = sorted(jaringan.titik.values(), key=lambda t: t.urgensi, reverse=True)
            for i, t in enumerate(urut, 1):
                print(f"  {i:2d}. {t.nama:<12} Urgensi: {t.urgensi}")
            print("\n  Semakin tinggi urgensi, semakin prioritas pengiriman.")
            print()

        elif pilihan == "0":
            print("\n  Terima kasih. Sistem siaga bencana selesai.")
            break

        else:
            print("  Pilihan tidak valid.")

        input("  Tekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    menu()
