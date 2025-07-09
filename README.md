# 🛡️ GTPDOOR Malware Overview

## 1. Ringkasan Umum
- **GTPDOOR** adalah malware berbasis **Linux** yang menargetkan sistem jaringan telekomunikasi, khususnya di sekitar **GRX (GPRS Roaming Exchange)**.
- Berfungsi sebagai **stealth backdoor** menggunakan **pesan GTP-C** sebagai saluran Command and Control (C2).
- Malware ini dapat dieksekusi dan dikendalikan dari luar tanpa membuka port mencurigakan.

## 2. Komunikasi & Mekanisme C2
- **Protokol**: GTP-C (control plane dari GPRS).
- **Media C2**: Disisipkan dalam GTP-C **Echo Request/Response** (type 0x01).
- **Teknik penyamaran**: Menggunakan **raw socket** dan **header TCP** untuk menyembunyikan beacon.
- **Payload terenkripsi** dengan algoritma XOR sederhana (default key: `135798642`).

## 3. Kemampuan & Fitur

### Fitur Dasar (Versi 1 & 2)
- Eksekusi perintah shell dari GTP Echo Request.
- Menyamar sebagai proses `syslogd`.
- Menulis data ke `system.conf`.
- Kompatibel dengan sistem lama (Red Hat Linux 4.1, GCC 2008).
- Tidak memerlukan konfigurasi firewall tambahan jika port GTP-C diizinkan.

### Fitur Tambahan Versi 2
- **Multithreaded**: Tangani GTP magic packet dan stealth TCP probe.
- **Access Control List (ACL)** berbasis IP/Subnet.
- **Rekeying runtime**: Ganti kunci enkripsi saat runtime.
- **Stealth TCP probing**: Respon TCP probe dengan beacon (RST+ACK, urgent pointer = 1).

## 4. Struktur Paket GTPDOOR

[ip_header] + [udp_header]
└─ [gtp_header]
├─ flags
├─ type (misal: 0x01 = Echo Request)
├─ length
└─ tei (biasanya tidak dipakai)
└─ [gtpdoor_header]
├─ pad[5]
├─ key1
├─ cmdMsgType
├─ cmdLength
└─ payload[2020]

markdown
Copy
Edit

## 5. Tipe Pesan & Perintah

### Versi 1
- `0x01`: Ganti kunci enkripsi
- `0x02`: Tulis data ke system.conf
- `0x03 - 0xFF`: Jalankan shell command

### Versi 2
- `0x01 - 0x02`: Sama seperti versi 1
- `0x03, 0x04, 0x08 - 0xFF`: Jalankan shell command
- `0x05`: Tambah IP/Subnet ke ACL
- `0x06`: Ambil daftar ACL
- `0x07`: Hapus ACL

## 6. Stealth Beacon via TCP

### Tujuan
- Izinkan remote scanning tanpa memicu deteksi dari firewall/stateful IDS.

### Mekanisme
- **Jika IP tidak ada di ACL**, maka malware merespons:
  - `TCP RST + ACK` dengan **urgent pointer = 1** (tanda aktif).
- **Jenis scan yang didukung**:
  - **TCP Connect Scan**: balasan RST+ACK saat ACK dikirim.
  - **TCP ACK Scan**: cukup kirim ACK → malware balas jika aktif.

### Teknik Covert
- Urgent pointer digunakan **tanpa mengaktifkan URG flag**.
- Teknik ini **tidak lazim secara RFC0793**, sehingga sukar dideteksi.

## 7. Target & Penempatan
- Target utama: sistem dengan koneksi langsung ke GRX:
  - `eDNS`, `SGSN`, `GGSN`, `PGW`, `STP`, `DRA`.
- Penempatan optimal: node yang memproses GTP-C.
- Bisa menyusup ke jaringan inti jika konfigurasi firewall GRX lemah.

## 8. Asosiasi & Afiliasi
- Diduga dikembangkan oleh grup **LIMINAL PANDA**.
- Nama lain:
  - **UNC1945** (versi Mandiant)
  - **LightBasin** (versi CrowdStrike)
- Teknik sebelumnya: encapsulasi `tinyshell` dalam sesi PDP menggunakan emulator SGSN.

## 9. Sampel & Analisis VirusTotal

### Versi 1
- Nama file: `dbus-echo`
- Arsitektur: x86-64
- SHA-256: `827f41fc1a6f8a4c8a8575b3e2349aeaba0dfc2c9390ef1cceeef1bb85c34161`

### Versi 2
- Nama file: `pickup`
- Arsitektur: i386
- SHA-256: `5cbafa2d562be0f5fa690f8d551cdb0bee9fc299959b749b99d44ae3fda782e4`

### Status Deteksi (per Maret 2024)
- Versi 1: naik dari 1 ke 37 deteksi
- Versi 2: dari 0 ke 37 deteksi

## 10. Eksekusi di Sistem

```bash
bash
nohup ./gtpdoor 2>&1 2>/dev/null &
Membuat mutex file: /var/run/daemon.pid

Menolak SIGCHLD untuk hindari zombie process

11. Kelemahan & Kerentanan
Target sistem lama tanpa patch.

Tersamar sebagai proses sistem.

GRX sebagai vector utama karena sifatnya tertutup dan lintas operator.

Potensi eksploitasi melalui info dari dokumen GSMA IR.21 (berisi IP/APN/GT).

📝 Catatan: Sampai saat ini, GTPDOOR belum terdokumentasi secara luas di forum publik. Temuan ini bisa menjadi indikator serangan baru terhadap infrastruktur telekomunikasi global.
