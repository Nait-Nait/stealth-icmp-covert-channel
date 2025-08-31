import argparse
import time
import os
import string
import random
import struct 
from scapy.all import IP, ICMP, Raw, send 

def build_payload(char: str, target_len: int) -> bytes:
    if target_len == 0:
        return char.encode("utf-8")

    timestamp = struct.pack("d", time.time())
    char_byte = char.encode("utf-8")
    padding_len = target_len - len(timestamp) - len(char_byte)
    patron = (string.ascii_letters + string.digits).encode("utf-8")
    padding = (patron * (padding_len // len(patron) + 1))[:padding_len]
    payload = timestamp + char_byte + padding

    return payload

def main():
    p = argparse.ArgumentParser(description="ICMP stealth sender (un char por paquete).")
    p.add_argument("--dst", required=True, help="IP destino (127.0.0.1 o tu gateway, p.ej. 192.168.1.1)")
    p.add_argument("--texto-cifrado", required=True, help="Texto YA cifrado (de caesar.py)")
    p.add_argument("--sleep", type=float, default=1.0, help="Segundos entre paquetes (default 1.0)")
    p.add_argument("--ttl", type=int, default=64, help="TTL típico en Linux (64)")
    p.add_argument("--icmp-id", type=int, default=os.getpid() & 0xFFFF, help="ICMP identifier (por defecto, PID)")
    p.add_argument("--seq-start", type=int, default=1, help="ICMP sequence inicial (default 1)")
    p.add_argument(
        "--payload-bytes",
        type=int,
        default=56,
        help="Tamaño del campo data en bytes (56 ≈ ping Linux por defecto). Usa 0 para sin padding.",
    )
    args = p.parse_args()

    msg = args.texto_cifrado
    if not msg.endswith("b"):
        msg += "b" 

    seq = args.seq_start

    for ch in msg:
        payload = build_payload(ch, args.payload_bytes)
        pkt = IP(dst=args.dst, ttl=args.ttl) / ICMP(type=8, id=args.icmp_id, seq=seq) / Raw(load=payload)

        send(pkt, verbose=False)

        print(f"TX -> dst={args.dst} icmp_id={args.icmp_id} seq={seq} ttl={args.ttl} char='{ch}' "
              f"payload_len={len(payload)}")
        seq += 1
        time.sleep(args.sleep)

if __name__ == "__main__":
    main()