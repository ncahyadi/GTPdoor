# 🧠 Hypothesis Tree: GTPdoor Campaign (APT-Level Analysis)

## 🌳 Main Hypothesis (Level 1)
> **Ada kampanye APT aktif yang menyusup ke core network Telco melalui penyalahgunaan protokol GTP dan komunikasi covert ICMP, dengan tujuan jangka panjang seperti pengendalian, eksfiltrasi, atau persistent access.**

---

## 🌿 Branch 1: Entry Point

### 1A. Abuse GTP-C traffic from internal misconfigured node
- GTPdoor planted di node bukan SGSN tapi bisa generate GTP
- 📌 **Evidence**:
  - GTP-C traffic dari IP internal non-SGSN
  - Tidak ada log GTP dari node resmi

### 1B. Insider planting via misused access
- Pegawai/insider install artefak secara lokal
- 📌 **Evidence**:
  - YARA hit hanya di subset host tertentu
  - Tidak ada komunikasi luar sebelum file muncul

### 1C. External access via exposed signaling interface
- Port GTP atau ICMP terbuka di perimeter
- 📌 **Evidence**:
  - PCAP menunjukkan GTP/ICMP dari IP luar
  - TTL abnormal

---

## 🌿 Branch 2: Tooling & Payload

### 2A. GTPdoor sebagai dropper dan covert channel
- Meniru behavior SGSN dan memanfaatkan channel tersembunyi
- 📌 **Evidence**:
  - Layer GTP traffic terlihat normal
  - Burst ICMP dari host yang sama

### 2B. Penggunaan SGSNEmu untuk masquerading / persistence
- Menyamarkan diri sebagai service SGSN
- 📌 **Evidence**:
  - Process name atau path menyerupai SGSN
  - Tidak ada binary SGSN resmi

### 2C. Fileless implant (memory resident)
- Tidak meninggalkan jejak di disk
- 📌 **Evidence**:
  - YARA hit tapi tidak ada file
  - Artefak volatile di RAM/heap/swap

---

## 🌿 Branch 3: Tujuan Aktor

### 3A. Exfiltrasi metadata pelanggan atau signaling log
- Target: CDR, HLR, SGSN logs
- 📌 **Evidence**:
  - Outbound ICMP mengandung pola structured data
  - Akses ke signaling DB/log

### 3B. Persistence jangka panjang
- Tetap dalam sistem tanpa terdeteksi
- 📌 **Evidence**:
  - Autostart (task schedule, service)
  - Survive reboot

### 3C. Lateral movement ke node telco lain
- Eksplorasi lebih luas di core network
- 📌 **Evidence**:
  - GTP lateral traffic
  - Auth trial ke node lain (HSS, GGSN, dll)

---

## 🌿 Branch 4: Threat Actor Archetype

### 4A. LightBasin-style (telco specific, SGSNEmu, covert ICMP)
- 📚 Referensi: CrowdStrike, Lookout
- Pattern cocok dengan abuse signaling, masking, dan persistence

### 4B. GALLIUM-style (SoftCell, deep persistent surveillance)
- Fokus ke metadata dan akses jangka panjang
- 📚 Referensi: Mandiant, Microsoft

### 4C. Unknown actor (emerging threat / local APT / insider sponsored)
- Masih butuh profiling lebih lanjut

---

## 🧭 Visual Structure (Text)

Main Hypothesis
│
├── Entry Point
│ ├── Misconfigured Node
│ ├── Insider Access
│ └── Exposed Interface
│
├── Tooling
│ ├── GTPdoor + ICMP
│ ├── SGSNEmu Masquerade
│ └── Fileless Implant
│
├── Objectives
│ ├── Metadata Exfil
│ ├── Long-Term Persistence
│ └── Lateral Movement
│
└── Actor Archetype
├── LightBasin
├── GALLIUM
└── Unknown


---

✅ **Catatan**: Pohon hipotesis ini bersifat *living document*. Update secara berkala berdasarkan artefak, log, traffic pattern, dan investigasi host/network yang sedang berjalan.

