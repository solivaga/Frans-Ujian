import requests
import threading
import time

# --- Konfigurasi Klien ---
BASE_API_URL = "http://127.0.0.1:5000"

# Data untuk diuji oleh klien: Daftar ISBN buku yang akan dicek
ISBN_UNTUK_DICEK = [
    "978-1408855652",
    "978-0261102217",
    "999-9999999999",
    "978-0321765723",
]  # Satu ISBN tidak ada


# ==============================================================================
# SOAL: Implementasi Fungsi untuk Cek Ketersediaan Buku via API
# ==============================================================================
def client_cek_buku_via_api(isbn, thread_name):
    """
    TUGAS ANDA:
    Lengkapi fungsi ini untuk mengambil informasi ketersediaan buku dari API
    dan mencetak hasilnya ke konsol.

    Langkah-langkah:
    1. Bentuk URL target: f"{BASE_API_URL}/buku/{isbn}/ketersediaan"
    2. Cetak pesan ke konsol bahwa thread ini ('thread_name') memulai pengecekan untuk 'isbn'.
       Contoh: print(f"[{thread_name}] Mengecek buku ISBN: {isbn}")
    3. Gunakan blok 'try-except' untuk menangani potensi error saat melakukan permintaan HTTP.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke URL target menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan data JSON dari 'response.json()'.
                  - Cetak judul dan status buku ke konsol.
                    Contoh: print(f"[{thread_name}] Buku '{data.get('judul')}': Status {data.get('status')}")
              - Jika 404 (buku tidak ditemukan):
                  - Cetak pesan bahwa buku tidak ada di katalog.
                    Contoh: print(f"[{thread_name}] Buku dengan ISBN {isbn} tidak ada di katalog.")
              - Untuk status code lain:
                  - Cetak pesan error umum ke konsol.
       b. Di blok 'except requests.exceptions.Timeout':
          - Cetak pesan bahwa permintaan timeout ke konsol.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Cetak pesan error permintaan umum ke konsol.
    4. Setelah blok try-except, cetak pesan ke konsol bahwa thread ini ('thread_name') selesai memproses 'isbn'.
    """
    target_url = f"{BASE_API_URL}/buku/{isbn}/ketersediaan"
    print(f"[{thread_name}] Mengecek buku ISBN: {isbn}")
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(
                f"[{thread_name}] Buku '{data.get('judul')}': Status {data.get('status')}"
            )
        elif response.status_code == 404:
            print(f"[{thread_name}] Buku dengan ISBN {isbn} tidak ada di katalog.")
        else:
            print(
                f"[{thread_name}] Terjadi error (status code: {response.status_code}) saat mengecek buku."
            )
    except requests.exceptions.Timeout:
        print(f"[{thread_name}] Permintaan timeout saat mengecek buku ISBN {isbn}.")
    except requests.exceptions.RequestException as e:
        print(f"[{thread_name}] Error permintaan: {e}")
    print(f"[{thread_name}] Selesai memproses buku ISBN: {isbn}")


def client_cek_antrean_via_api(id_antrean, thread_name):
    """
    Fungsi untuk mengambil status antrean dari API dan mencetak hasilnya ke konsol.
    """
    target_url = f"{BASE_API_URL}/antrean/{id_antrean}/status"
    print(f"[{thread_name}] Mengecek status antrean ID: {id_antrean}")
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(
                f"[{thread_name}] Antrean '{data.get('nama')}': Status {data.get('status')}"
            )
        elif response.status_code == 404:
            print(f"[{thread_name}] Antrean dengan ID {id_antrean} tidak ditemukan.")
        else:
            print(
                f"[{thread_name}] Terjadi error (status code: {response.status_code}) saat mengecek antrean."
            )
    except requests.exceptions.Timeout:
        print(
            f"[{thread_name}] Permintaan timeout saat mengecek antrean ID {id_antrean}."
        )
    except requests.exceptions.RequestException as e:
        print(f"[{thread_name}] Error permintaan: {e}")
    print(f"[{thread_name}] Selesai memproses antrean ID: {id_antrean}")


# --- Bagian Utama Skrip (Tidak Perlu Diubah Peserta) ---
if __name__ == "__main__":
    print(
        f"Memulai Klien Pengecek untuk {len(ISBN_UNTUK_DICEK)} Buku Secara Concurrent."
    )

    threads = []
    start_time = time.time()

    for i, isbn_cek in enumerate(ISBN_UNTUK_DICEK):
        thread_name_for_task = f"Mahasiswa-{i+1}"

        thread = threading.Thread(
            target=client_cek_buku_via_api, args=(isbn_cek, thread_name_for_task)
        )
        threads.append(thread)
        thread.start()

    for thread_instance in threads:
        thread_instance.join()

    end_time = time.time()
    total_time = end_time - start_time

    print(
        f"\nSemua pengecekan buku telah selesai diproses dalam {total_time:.2f} detik."
    )
