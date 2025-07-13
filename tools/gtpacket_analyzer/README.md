# 🛰️ GTP Packet Analyzer & SGSNemu Detector

Python script ini digunakan untuk menganalisis packet GTP (GPRS Tunneling Protocol) dari input berupa **hex string**, dengan fitur-fitur keamanan dan deteksi ancaman tersembunyi seperti **GTPdoor**, **tunneling tersembunyi**, serta deteksi heuristik terhadap **SGSNemu** (emulator SGSN).

---

## 🚀 Cara Penggunaan

1. Jalankan script menggunakan Python 3:
   ```bash
   python3 gtp_analyzer.py
   ```

2. Masukkan hex string dari packet GTP saat diminta. Contoh input:
   ```
   32 01 00 08 00 00 00 00 47 44 01 02 03 04
   ```

---

## 🔍 Fitur Utama

### ✅ GTP Header Parser
- Menampilkan informasi:
  - **Version**
  - **Flags** (E, S, PN)
  - **Message Type**
  - **TEID**
  - **Payload Length**

### 🧪 Payload Analyzer
- **Entropy Calculation** untuk mengukur keacakan data.
- **Signature Matching** untuk mendeteksi GTPdoor (`0x47 0x44` / `GD`).
- **Tunneling Detection**:
  - ICMP-over-GTP (indikasi byte 0x08, 0x00)
  - DNS-over-GTP (indikasi byte 0x00, 0x35)
- **Fragmentation Detection** untuk payload berukuran sangat kecil.
- **ASCII Extraction** jika payload mengandung karakter yang dapat dicetak.

### 🛰️ SGSNemu Heuristic Detector
- Deteksi heuristik jika:
  - Message Type = Echo Request (`0x01`)
  - TEID = `0x00000000`
  - Tidak ada Extension Header, Sequence Number, dan N-PDU

---

## 🧾 Contoh Output

```
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

[+] Payload Extracted (8 bytes): 47 44 01 02 03 04

=== [Payload Analysis] ===
[+] Entropy: 2.2500 bits/byte
[+] GTPdoor signature: FOUND ('GD' magic bytes)
[?] ICMP Tunneling Suspicion: Possible
[.] DNS-over-GTP Suspicion: Unlikely
[?] Fragmented Payload: YES (possible reassembly needed)
[+] ASCII Printable: GD....
```

---

## 📦 Dependencies

Script ini **tidak memerlukan pustaka eksternal** dan hanya menggunakan modul bawaan Python 3.

---

## ⚠️ Catatan

- Deteksi SGSNemu bersifat **heuristik** dan digunakan sebagai indikasi awal, bukan bukti mutlak.
- Analisis ini cocok untuk threat hunting, investigasi, dan reverse engineering di lingkungan GTP (seperti mobile core network / telco environments).
- Cocok digunakan dalam riset ancaman seperti **stealth passive backdoor**, **covert channel**, dan **GTP abuse**.

---
