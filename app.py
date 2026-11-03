from flask import Flask, abort, redirect, url_for

app = Flask(__name__)

# ===== Kelompok 1: data contoh =====
ALAT = [
    {"id": 1, "nama": "Tenda Dome 4 Orang", "kategori": "tenda", "tarif": 60000, "stok": 3},
    {"id": 2, "nama": "Carrier 60 Liter", "kategori": "tas", "tarif": 25000, "stok": 5},
    {"id": 3, "nama": "Kompor Portable", "kategori": "alat masak", "tarif": 10000, "stok": 4},
    {"id": 4, "nama": "Sleeping Bag", "kategori": "tidur", "tarif": 15000, "stok": 0},
    {"id": 5, "nama": "Headlamp", "kategori": "penerangan", "tarif": 8000, "stok": 6},
    {"id": 6, "nama": "Jaket Gunung", "kategori": "pakaian", "tarif": 20000, "stok": 2},
]

PENYEWA = {
    "rina_hiker": {"nama": "Rina Maharani", "kota": "Malang", "jumlah_sewa": 7},
    "bayu99": {"nama": "Bayu Prakoso", "kota": "Surabaya", "jumlah_sewa": 2},
    "dina_trail": {"nama": "Dina Safitri", "kota": "Pasuruan", "jumlah_sewa": 5},
    "gilang_s": {"nama": "Gilang Saputra", "kota": "Sidoarjo", "jumlah_sewa": 1},
}

USERNAME_DILARANG = ["admin", "petugas", "gudang"]


# ===== Kelompok 2: fungsi bantu =====
def rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")


def bungkus(judul, isi):
    """Membungkus isi halaman dengan judul dan menu navigasi yang sama."""
    menu = (
        f'<a href="{url_for("beranda")}">Beranda</a> | '
        f'<a href="{url_for("tentang")}">Tentang</a> | '
        f'<a href="{url_for("katalog")}">Katalog</a> | '
        f'<a href="{url_for("kontak")}">Kontak</a>'
    )
    return f"<h1>{judul}</h1><nav>{menu}</nav><hr>{isi}"


def cek_format(username):
    """Mengembalikan (True, "") bila format sah, atau (False, alasan) bila tidak."""
    if len(username) < 4 or len(username) > 16:
        return False, "Username harus 4 sampai 16 karakter."
    if username[0].isdigit():
        return False, "Username tidak boleh diawali angka."
    if not (username.isascii() and username.replace("_", "").isalnum()):
        return False, "Username hanya boleh berisi huruf, angka, dan garis bawah."
    if username.lower() in USERNAME_DILARANG:
        return False, "Username ini dicadangkan dan tidak boleh dipakai."
    return True, ""


# ===== Kelompok 3: route statis =====
@app.route("/")
def beranda():
    contoh = url_for("cek_username", username="rina_hiker")
    isi = (
        "<p>Sewa perlengkapan naik gunung dengan harga bersahabat.</p>"
        f'<p>Coba cek username contoh: <a href="{contoh}">rina_hiker</a></p>'
    )
    return bungkus("Rental alat hiking ala Rehan", isi)


@app.route("/tentang")
def tentang():
    isi = (
        "<p>Basecamp buka setiap hari pukul 06.30 sampai 20.00.</p>"
        "<p>Aturan sewa: jaminan KTP, denda keterlambatan 50% tarif per hari.</p>"
    )
    return bungkus("Tentang Kami", isi)


@app.route("/katalog")
def katalog():
    baris = ""
    for alat in ALAT:
        tautan = url_for("detail_alat", alat_id=alat["id"])
        baris += f'<li><a href="{tautan}">{alat["nama"]}</a> - {rupiah(alat["tarif"])}/hari</li>'
    return bungkus("Katalog Alat", f"<ul>{baris}</ul>")


@app.route("/kontak")
def kontak():
    isi = "<p>WhatsApp: 0812-0000-0000<br>Alamat: Jl. Basecamp No. 1, Malang</p>"
    return bungkus("Kontak", isi)


# Alamat pendek yang dialihkan ke katalog
@app.route("/alat")
def alias_katalog():
    return redirect(url_for("katalog"))


# ===== Kelompok 4: route dengan converter int =====
@app.route("/katalog/<int:alat_id>")
def detail_alat(alat_id):
    for alat in ALAT:
        if alat["id"] == alat_id:
            status = f"Tersedia ({alat['stok']} unit)" if alat["stok"] > 0 else "Sedang disewa"
            isi = (
                f"<p>Kategori: {alat['kategori']}</p>"
                f"<p>Tarif: {rupiah(alat['tarif'])} per hari</p>"
                f"<p>Status: {status}</p>"
            )
            return bungkus(alat["nama"], isi)
    abort(404)


# ===== Kelompok 5: dynamic route dengan validasi =====
@app.route("/cek/<username>")
def cek_username(username):
    valid, alasan = cek_format(username)
    if not valid:
        return bungkus("Username Tidak Valid", f"<p>{alasan}</p>")

    if username.lower() not in PENYEWA:
        isi = f"<p>Format <b>{username}</b> sah, tetapi belum terdaftar sebagai penyewa.</p>"
        return bungkus("Belum Terdaftar", isi)

    # username sah dan terdaftar: arahkan ke halaman profilnya
    return redirect(url_for("profil_penyewa", username=username.lower()))


@app.route("/user/<username>")
def profil_penyewa(username):
    valid, alasan = cek_format(username)
    if not valid:
        return bungkus("Username Tidak Valid", f"<p>{alasan}</p>"), 400

    data = PENYEWA.get(username.lower())
    if data is None:
        abort(404)

    label = "Member setia" if data["jumlah_sewa"] >= 5 else "Penyewa baru"
    isi = (
        f"<p>Nama: {data['nama']}</p>"
        f"<p>Kota: {data['kota']}</p>"
        f"<p>Jumlah sewa: {data['jumlah_sewa']} kali ({label})</p>"
    )
    return bungkus(f"Profil @{username.lower()}", isi)


# ===== Kelompok 6: halaman 404 kustom dan penjalan server =====
@app.errorhandler(404)
def jalur_tidak_ditemukan(error):
    isi = (
        "<p>Jalur yang kamu cari tidak ada di peta kami.</p>"
        f'<p><a href="{url_for("beranda")}">Kembali ke basecamp</a></p>'
    )
    return bungkus("404 - Jalur Tidak Ditemukan", isi), 404


if __name__ == "__main__":
    app.run(debug=True)
