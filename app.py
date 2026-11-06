from flask import Flask, abort, redirect, render_template, url_for

app = Flask(__name__)

NAMA_USAHA = "Rental Alat Hiking ala Rehan"

# ===== Kelompok 1: data data=====
ALAT = [
    {"id": 1, "nama": "Tenda Dome 4 Orang", "kategori": "tenda", "tarif": 60000, "stok": 3, 
     "deskripsi": "Tenda dome 4 orang, cocok untuk keluarga atau kelompok kecil serta tahan angin dan hujan."},
    {"id": 2, "nama": "Carrier 60 Liter", "kategori": "tas", "tarif": 25000, "stok": 5, 
     "deskripsi": "Tas gunung dengan frame dan rain cover, nyaman untuk bawaan beberapa hari."},
    {"id": 3, "nama": "Kompor Portable", "kategori": "alat masak", "tarif": 10000, "stok": 4, 
     "deskripsi": "Kompor gas kecil portabel, mudah dibawa dan digunakan di alam terbuka."},
    {"id": 4, "nama": "Sleeping Bag", "kategori": "tidur", "tarif": 15000, "stok": 0, 
     "deskripsi": "Kantong tidur hangat, cocok untuk suhu dingin di pegunungan."},
    {"id": 5, "nama": "Headlamp", "kategori": "penerangan", "tarif": 8000, "stok": 6, 
     "deskripsi": "Lampu kepala LED dengan 3 mode cahaya, tahan air dan baterai tahan lama."},
    {"id": 6, "nama": "Jaket Gunung", "kategori": "pakaian", "tarif": 20000, "stok": 2, 
     "deskripsi": "Jaket windproof dan waterproof, ringan mudah dilipat dan dibawa."},
]

PENYEWA = {
    "rina_hiker": {"nama": "Rina Maharani", "kota": "Malang", "jumlah_sewa": 7},
    "bayu99": {"nama": "Bayu Prakoso", "kota": "Surabaya", "jumlah_sewa": 2},
    "dina_trail": {"nama": "Dina Safitri", "kota": "Pasuruan", "jumlah_sewa": 5},
    "gilang_s": {"nama": "Gilang Saputra", "kota": "Sidoarjo", "jumlah_sewa": 1},
}

USERNAME_DILARANG = ["admin", "petugas", "gudang"]


# ===== Kelompok 2: filter, variabel global, dan validasi=====
@app.template_filter("rupiah")
def rupiah(angka):
    """flter Jinja2 buatan sendiri: {{ 60000 | rupiah }} menjadi "Rp 60.000"."""
    return "Rp " + f"{angka:,}".replace(",", ".")



@app.context_processor
def data_global():
    return {"nama_usaha": NAMA_USAHA}


def cek_format(username):
    """Mengembalikan (True, "") bila format sah, atau (False, alasan) bila tidak."""
    if len(username) <  4 or len(username) >16:
        return False, "Username harus 4 sampai 16 karakter."
    if username[0].isdigit():
        return False, "Username tidak boleh diawali angka."
    if not (username.isascii() and username.replace("_", "").isalnum()):
        return False, "Username hanya boleh berisi huruf, angka, dan garis bawah."
    if username.lower() in USERNAME_DILARANG:
        return False, "username ini dicadangkan dan tidak boleh dipakai."
    return True, ""


# ==== kelompok 3: route biasa ====
@app.route("/")
def beranda():
    return render_template("index.html")


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/katalog")
def katalog():
    return render_template("katalog.html", daftar_alat=ALAT)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html")


@app.route("/alat")
def alias_katalog():
    return redirect(url_for("katalog"))


# ===== Kelompok 4: detail alat =====
@app.route("/katalog/<int:alat_id>")
def detail_alat(alat_id):
    for alat in ALAT:
        if alat["id"] == alat_id:
            return render_template("detail.html", alat=alat)
    abort(404)


# ===== Kelompok 5: cek username dan profil penyewa=====
@app.route("/cek/<username>")
def cek_username(username):
    u = username.lower()
    valid, alasan = cek_format(username)
    tersedia = valid and u not in PENYEWA
    return render_template(
        "cek.html", username=username, valid=valid, alasan=alasan, tersedia=tersedia
    )


@app.route("/user/username>")
def profil_penyewa(username):
    u = username.lower()
    valid, alasan = cek_format(username)
    if not valid:
        return render_template(
            "cek.html", username=username, valid=False, alasan=alasan, tersedia=False
        ), 400

    penyewa = PENYEWA.get(u)
    if penyewa is None:
        abort(404)
    return render_template("profil.html", username=u, penyewa=penyewa)


# ===== Kelompok 6: halaman 404 dan perjalan server =====
@app.errorhandler(404)
def jalur_tidak_ditemukan(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
