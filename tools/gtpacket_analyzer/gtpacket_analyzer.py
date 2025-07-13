import binascii
import math
from collections import Counter

def hex_to_bytes(hex_str):
    """Ubah hex string (dengan atau tanpa spasi) ke byte array."""
    hex_str = ''.join(hex_str.strip().split())  # hapus whitespace
    return bytes.fromhex(hex_str)

def calculate_entropy(data):
    """Hitung entropi Shannon dari byte data."""
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
    return entropy

def is_possible_icmp(data):
    """Cek apakah payload cocok dengan pola ICMP (misal 08 00 = Echo Request)."""
    return len(data) > 2 and data[0] in [0x08, 0x00] and data[1] == 0x00

def is_possible_dns(data):
    """Cek apakah payload cocok dengan pola DNS header (TXID + QR = 0)."""
    return len(data) > 12 and (data[2] & 0x80) == 0x00

def detect_gtpdoor_signature(data):
    """Deteksi signature GTPdoor, contoh: magic byte 'GD' (0x47 0x44)."""
    return data.startswith(b'GD')

def detect_fragmentation(data):
    """Asumsi fragmentasi jika payload sangat kecil (<20 byte)."""
    return len(data) < 20

def parse_gtp_packet(gtp_bytes):
    """Parse GTPv1 header dan ekstrak payload."""
    if len(gtp_bytes) < 8:
        raise ValueError("Packet terlalu pendek untuk valid GTP")

    print("\n=== [GTP Header Parsing] ===")
    flags = gtp_bytes[0]
    version = (flags & 0b11100000) >> 5
    pt = (flags & 0b00010000) >> 4
    e_flag = (flags & 0b00000100) >> 2
    s_flag = (flags & 0b00000010) >> 1
    pn_flag = (flags & 0b00000001)

    msg_type = gtp_bytes[1]
    length = int.from_bytes(gtp_bytes[2:4], byteorder='big')
    teid = gtp_bytes[4:8]

    pt_str = "GTP-U (User Plane)" if pt else "GTP-C (Control Plane)"
    msg_desc = "Echo Request" if msg_type == 0x01 else "Other"

    print(f"[+] Flags: 0x{flags:02X}")
    print(f"    - Version: {version}")
    print(f"    - Protocol Type (PT): {pt} → {pt_str}")
    print(f"    - E flag (Ext Header): {e_flag}")
    print(f"    - S flag (Seq Num): {s_flag}")
    print(f"    - PN flag (N-PDU Num): {pn_flag}")
    print(f"[+] Message Type: 0x{msg_type:02X} ({msg_desc})")
    print(f"[+] Length (payload only): {length} bytes")
    print(f"[+] TEID: {teid.hex()}")

    # Deteksi kemungkinan SGSNemu
    print("\n=== [SGSNemu Detection] ===")
    suspicious_teid = teid == b'\x00\x00\x00\x00'
    minimal_header = e_flag == 0 and s_flag == 0 and pn_flag == 0
    is_echo = msg_type == 0x01

    if suspicious_teid and minimal_header and is_echo:
        print("[+] SGSNemu Signature: HIGHLY SUSPICIOUS (Echo Request, TEID=0, Minimal Header)")
    else:
        print("[-] SGSNemu Signature: Not clearly identified")

    header_len = 8
    payload = gtp_bytes[header_len:header_len + length]
    print(f"[+] Payload Extracted ({len(payload)} bytes): {payload.hex()}")

    return payload

def analyze_payload(payload):
    """Analisis payload: entropi, signature, tunneling, fragmentasi."""
    print("\n=== [Payload Analysis] ===")
    entropy = calculate_entropy(payload)
    print(f"[+] Entropy: {entropy:.4f} bits/byte")

    if detect_gtpdoor_signature(payload):
        print("[+] GTPdoor signature: FOUND ('GD' magic bytes)")
    else:
        print("[-] GTPdoor signature: Not detected")

    if is_possible_icmp(payload):
        print("[?] ICMP Tunneling Suspicion: Possible")
    else:
        print("[.] ICMP Tunneling Suspicion: Unlikely")

    if is_possible_dns(payload):
        print("[?] DNS-over-GTP Suspicion: Possible")
    else:
        print("[.] DNS-over-GTP Suspicion: Unlikely")

    if detect_fragmentation(payload):
        print("[?] Fragmented Payload: YES (possible reassembly needed)")
    else:
        print("[.] Fragmented Payload: No")

    try:
        printable = payload.decode('ascii')
        print(f"[+] ASCII Printable: {printable}")
    except UnicodeDecodeError:
        print("[-] ASCII Printable: No (binary or obfuscated data)")

def main():
    print("=== GTP Packet Analyzer ===")
    hex_data = input("Masukkan hex data dari GTP packet (contoh: 32 01 00 08 00 00 00 00 47 44 01 02):\n> ")
    try:
        gtp_bytes = hex_to_bytes(hex_data)
        payload = parse_gtp_packet(gtp_bytes)
        analyze_payload(payload)
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()