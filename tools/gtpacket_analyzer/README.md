# GTP Packet Analyzer & SGSNemu Detector

Python script ini digunakan untuk menganalisis packet GTP (GPRS Tunneling Protocol) dari input berupa **hex string**, dengan fitur-fitur keamanan dan threat detection, khususnya untuk mendeteksi **GTPdoor**, tunneling tersembunyi, dan emulasi seperti **SGSNemu**.

---

## 🔧 Cara Penggunaan

1. Jalankan script:
   ```bash
   python3 gtp_analyzer.py
Masukkan hex string dari packet GTP saat diminta, contoh:

Copy
Edit
32 01 00 08 00 00 00 00 47 44 01 02 03 04
✨ Fitur Utama
GTP Header Parser
Menampilkan informasi lengkap dari header GTP: version, flags, TEID, message type, dan panjang payload.

Payload Analyzer
Melakukan analisis mendalam terhadap payload:

Perhitungan entropy

Deteksi signature GTPdoor (0x47 0x44)

Deteksi kemungkinan tunneling ICMP dan DNS-over-GTP

Deteksi fragmentasi

Ekstraksi ASCII (jika tersedia)

SGSNemu Detection (Heuristik)
Deteksi kemungkinan emulator SGSNemu berdasarkan karakteristik umum:

GTP-C Echo Request

TEID bernilai 0x00000000

Header minimal (tanpa extension, sequence, N-PDU)

📌 Output Contoh
yaml
Copy
Edit
=== [GTP Header Parsing] ===
[+] Flags: 0x32
    - Version: 1
    - Protocol Type (PT): 1 → GTP-U (User Plane)
    - E flag (Ext Header): 0
    - S flag (Seq Num): 1
    - PN flag (N-PDU Num): 0
[+] Message Type: 0x01 (Echo Request)
[+] Length (payload only): 8 bytes
[+] TEID: 00000000

=== [SGSNemu Detection] ===
[+] SGSNemu Signature: HIGHLY SUSPICIOUS (Echo Request, TEID=0, Minimal Header)

[+] Payload Extracted (8 bytes): 474401020304

=== [Payload Analysis] ===
[+] Entropy: 2.2500 bits/byte
[+] GTPdoor signature: FOUND ('GD' magic bytes)
[?] ICMP Tunneling Suspicion: Possible
[.] DNS-over-GTP Suspicion: Unlikely
[?] Fragmented Payload: YES (possible reassembly needed)
[+] ASCII Printable: GD...
⚠️ Catatan
Script ini ditujukan untuk analisis pasif terhadap log packet GTP dalam konteks investigasi ancaman seperti stealthy backdoor atau data exfiltration via tunneling.

Deteksi SGSNemu bersifat heuristik dan tidak konklusif, namun dapat membantu sebagai indikator awal adanya aktivitas mencurigakan.

Tidak memerlukan pustaka eksternal tambahan (standar Python 3).
