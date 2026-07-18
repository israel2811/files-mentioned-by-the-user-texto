#!/usr/bin/env python3
"""Forensic UDP Monitor for NEXUS/CCA-AAV.

Listens for UDP packets on the local machine and logs metadata to a CSV file.
Requires Administrator privileges to use raw socket sniffing on Windows.
Falls back to a standard UDP socket listener on VoIP/RTP ports if raw sniffing fails.
"""

from __future__ import annotations

import csv
import os
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "forensic_udp_log.csv"
UDP_VOIP_PORTS = {5004, 5005, 5060, 5061, 8000, 16384}  # Common VoIP/RTP ports


def run_raw_sniffer():
    print("Attempting to initialize raw socket sniffer...")
    # Get local hostname and IP
    host = socket.gethostbyname(socket.gethostname())
    print(f"Binding to interface: {host}")
    
    # Create raw socket (IP protocol)
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((host, 0))
    
    # Include IP headers
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    # Enable Promiscuous Mode (Windows specific IOCTL)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    print("\nSniffer active. Logging all local UDP headers with millisecond precision...")
    print(f"Logging to: {LOG_FILE.resolve()}\n")
    print("Press Ctrl+C to stop.")
    
    # Write CSV Header
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Source_IP", "Source_Port", "Dest_IP", "Dest_Port", "Length"])
        
    try:
        while True:
            # Receive packet
            data, addr = s.recvfrom(65565)
            t = time.time()
            dt = datetime.fromtimestamp(t).isoformat(timespec="milliseconds")
            
            # Parse IPv4 Header
            ip_header = data[:20]
            iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
            protocol = iph[6]
            
            if protocol == 17:  # UDP Protocol
                # UDP Header is 8 bytes after IP Header (which is usually 20 bytes)
                version_header_len = ip_header[0]
                ip_header_len = (version_header_len & 0xF) * 4
                
                udp_header = data[ip_header_len : ip_header_len + 8]
                udph = struct.unpack("!HHHH", udp_header)
                src_port = udph[0]
                dest_port = udph[1]
                length = udph[2]
                
                src_ip = socket.inet_ntoa(iph[8])
                dest_ip = socket.inet_ntoa(iph[9])
                
                # Log entry
                with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([dt, src_ip, src_port, dest_ip, dest_port, length])
                    
                print(f"[{dt}] UDP: {src_ip}:{src_port} -> {dest_ip}:{dest_port} | Len: {length}")
                
    except KeyboardInterrupt:
        print("\nSniffer stopped by user.")
    except Exception as e:
        print(f"Error during raw sniffing: {e}")
    finally:
        # Disable Promiscuous Mode
        try:
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        except Exception:
            pass


def run_udp_listener():
    print("\n[Sniffer Fallback] Launching active UDP Listener...")
    print("Binding standard sockets to common VoIP/RTP ports to listen for traffic...")
    
    listeners = []
    for port in UDP_VOIP_PORTS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("0.0.0.0", port))
            s.setblocking(False)
            listeners.append((s, port))
            print(f"Listening on port {port} (VoIP/RTP)")
        except Exception as e:
            print(f"Could not bind port {port}: {e}")
            
    if not listeners:
        print("Error: Could not bind any UDP listener ports. Port conflict?")
        return
        
    print(f"\nListener active. Logging packets to: {LOG_FILE.name}")
    print("Press Ctrl+C to stop.")
    
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Local_Port", "Sender_IP", "Sender_Port", "Length"])
        
    try:
        while True:
            for s, port in listeners:
                try:
                    data, addr = s.recvfrom(2048)
                    t = time.time()
                    dt = datetime.fromtimestamp(t).isoformat(timespec="milliseconds")
                    sender_ip, sender_port = addr
                    length = len(data)
                    
                    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([dt, port, sender_ip, sender_port, length])
                        
                    print(f"[{dt}] Port {port} <- {sender_ip}:{sender_port} | Len: {length}")
                except BlockingIOError:
                    pass
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nListener stopped by user.")
    finally:
        for s, _ in listeners:
            s.close()


if __name__ == "__main__":
    import struct
    
    # Check for Admin rights (Windows specific check)
    is_admin = False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        print("="*70)
        print("WARNING: Python is running without Administrator privileges.")
        print("Raw packet sniffing requires elevated rights in Windows.")
        print("To run the raw sniffer, please launch PowerShell as Administrator and run:")
        print(f"  python {Path(__file__).name}")
        print("="*70)
        run_udp_listener()
    else:
        run_raw_sniffer()
