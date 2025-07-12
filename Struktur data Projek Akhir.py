import csv
from datetime import datetime
from collections import defaultdict

# File CSV untuk menyimpan data
nama_file = 'Keuangan Pribadi.csv'

# kategori pengeluaran menggunakan Hashmap
pengeluaran = {
    'makan': 'mengisi tenaga ',
    'transportasi': 'kendaraan',
    'hiburan': 'Kesenangan',
    'belanja': 'kebutuhan sehari-hari',
    'lainnya': 'Lain-lain'
}

# Fungsi mencatat transaksi
def transaksi(jenis, jumlah, kategori, tanggal):
    data = [tanggal, jenis, jumlah, kategori]
    with open(nama_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    print("Transaksi berhasil dicatat!")

# Fungsi membaca transaksi dari file
def baca_transaksi():
    transaksi = []
    try:
        with open(nama_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tanggal, jenis, jumlah, kategori = row
                transaksi.append({
                    'tanggal': tanggal,
                    'jenis': jenis,
                    'jumlah': float(jumlah),
                    'kategori': kategori
                })
    except FileNotFoundError:
        pass
    return transaksi

# Fungsi laporan bulanan
def laporan_bulanan(bulan, tahun):
    transaksi = baca_transaksi()
    pemasukan = pengeluaran = 0
    for tr in transaksi:
        tgl = datetime.strptime(tr['tanggal'], '%Y-%m-%d')
        if tgl.month == bulan and tgl.year == tahun:
            if tr['jenis'] == 'pemasukan':
                pemasukan += tr['jumlah']
            else:
                pengeluaran += tr['jumlah']
    print(f"\nLaporan Bulanan: {bulan}/{tahun}")
    print(f"Total Pemasukan : Rp{pemasukan:,.2f}")
    print(f"Total Pengeluaran : Rp{pengeluaran:,.2f}")
    print(f"Saldo Bersih : Rp{(pemasukan - pengeluaran):,.2f}")

# Fungsi laporan tahunan
def laporan_tahunan(tahun):
    transaksi = baca_transaksi()
    laporan = defaultdict(lambda: {'pemasukan': 0, 'pengeluaran': 0})
    for tr in transaksi:
        tgl = datetime.strptime(tr['tanggal'], '%Y-%m-%d')
        if tgl.year == tahun:
            bulan = tgl.month
            if tr['jenis'] == 'pemasukan':
                laporan[bulan]['pemasukan'] += tr['jumlah']
            else:
                laporan[bulan]['pengeluaran'] += tr['jumlah']
    
    print(f"\n Laporan Tahunan: {tahun}")
    for bulan in range(1, 13):
        pmsk = laporan[bulan]['pemasukan']
        pngl = laporan[bulan]['pengeluaran']
        print(f"Bulan {bulan}: Pemasukan Rp{pmsk:,.2f}, Pengeluaran Rp{pngl:,.2f}, Saldo Rp{(pmsk - pngl):,.2f}")

#hapus baris dengan konfirmasi kepada pengguna
def hapus_baris_konfirmasi():
    transaksi = baca_transaksi()

    if not transaksi:
        print("idak ada data yang dihapus.")
        return

    print("\nDaftar Transaksi:")
    for idx, tr in enumerate(transaksi):
        print(f"{idx + 1}. {tr['tanggal']} | {tr['jenis']} | Rp{tr['jumlah']:,.2f} | {tr['kategori']}")

    try:
        nomor = int(input("\nMasukkan nomor baris yang ingin dihapus: ")) - 1
        if 0 <= nomor < len(transaksi):
            tr = transaksi[nomor]
            konfirmasi = input(f"Yakin ingin menghapus baris ini? (y/n)\n{tr['tanggal']} | {tr['jenis']} | Rp{tr['jumlah']:,.2f} | {tr['kategori']}\n> ")
            if konfirmasi.lower() == 'y':
                del transaksi[nomor]
                with open(nama_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for tr in transaksi:
                        writer.writerow([tr['tanggal'], tr['jenis'], tr['jumlah'], tr['kategori']])
                print("Baris berhasil dihapus.")
            else:
                print("Dibatalkan.")
        else:
            print("Nomor baris tidak ada.")
    except ValueError:
        print("Input harus angka.")
        
# Fungsi utama
def main():
    while True:
        print("\n=== Manajemen Keuangan Pribadi ===")
        print("1. Catat Pemasukan")
        print("2. Catat Pengeluaran")
        print("3. Laporan Bulanan")
        print("4. Laporan Tahunan")
        print("5 hapus data")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jumlah = float(input("Masukkan jumlah pemasukan: Rp"))
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            transaksi('pemasukan', jumlah, '-', tanggal)

        elif pilihan == '2':
            jumlah = float(input("Masukkan jumlah pengeluaran: Rp"))
            print("Kategori (makan/transportasi/hiburan/belanja/lainnya):")
            kategori = input("Masukkan kategori: ").lower()
            if kategori not in pengeluaran:
                kategori = 'lainnya'
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            transaksi('pengeluaran', jumlah, kategori, tanggal)

        elif pilihan == '3':
            bulan = int(input("Masukkan bulan (1-12): "))
            tahun = int(input("Masukkan tahun (YYYY): "))
            laporan_bulanan(bulan, tahun)

        elif pilihan == '4':
            tahun = int(input("Masukkan tahun (YYYY): "))
            laporan_tahunan(tahun)

        elif pilihan == '5':
            hapus_baris_konfirmasi()

        elif pilihan == '0':
            print("Terima kasih telah menggunakan aplikasi ini.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == '__main__':
    main()