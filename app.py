import flask
from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# Database simulasi katalog buku
buku_db = {
    "978-0261102217": {"judul": "The Lord of The Rings", "status": "Dipinjam", "kembali_tgl": "2024-12-20"},
    "978-1408855652": {"judul": "Harry Potter and the Philosopher's Stone", "status": "Tersedia", "lokasi": "Rak Fiksi F-3"},
    "978-0321765723": {"judul": "The C++ Programming Language", "status": "Tersedia", "lokasi": "Rak Komputer C-1"},
    "978-0743273565": {"judul": "The Da Vinci Code", "status": "Dipinjam", "kembali_tgl": "2024-12-15"},
}
db_lock = threading.Lock()

def log_server_activity(message):
    """Fungsi sederhana untuk logging di sisi server (ke konsol)."""
    print(f"[SERVER-PERPUS] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

@app.route('/buku/<isbn>/ketersediaan', methods=['GET'])
def get_ketersediaan_buku(isbn):
    """Endpoint untuk mendapatkan ketersediaan buku berdasarkan ISBN."""
    log_server_activity(f"Permintaan ketersediaan untuk ISBN: {isbn}")
    
    time.sleep(random.uniform(0.1, 0.4)) 
    
    with db_lock:
        buku = buku_db.get(isbn)
    
    if buku:
        response_data = buku.copy()
        response_data["isbn"] = isbn
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Buku dengan ISBN tersebut tidak ada di katalog"}), 404

if __name__ == '__main__':
    log_server_activity("API Pengecek Ketersediaan Buku Perpustakaan Kota dimulai.")
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)