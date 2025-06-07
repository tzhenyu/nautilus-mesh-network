import socket
import threading
import time
import json
import os

BROADCAST_PORT = 50010
BROADCAST_INTERVAL = 5       # seconds
DISCOVERY_FILE = "/tmp/mesh_peers.json"
MESH_SUBNET = "192.168.199." # Adjust as needed

def get_ip():
    import subprocess
    try:
        result = subprocess.check_output("hostname -I", shell=True)
        for ip in result.decode().split():
            if ip.startswith(MESH_SUBNET):
                return ip
        return None
    except Exception:
        return None

def broadcaster(hostname, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        msg = json.dumps({"hostname": hostname, "ip": ip})
        s.sendto(msg.encode(), ('<broadcast>', BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)

def listener(my_hostname, my_ip, peers):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', BROADCAST_PORT))
    while True:
        data, addr = s.recvfrom(1024)
        try:
            msg = json.loads(data.decode())
            host, ip = msg.get("hostname"), msg.get("ip")
            if ip and host and ip != my_ip:
                peers[ip] = host
                # Save to file for use by status sender
                with open(DISCOVERY_FILE, "w") as f:
                    json.dump(peers, f)
        except Exception:
            continue

def main():
    hostname = socket.gethostname()
    ip = get_ip()
    if not ip:
        print("No mesh IP found.")
        return
    peers = {}
    t1 = threading.Thread(target=broadcaster, args=(hostname, ip), daemon=True)
    t2 = threading.Thread(target=listener, args=(hostname, ip, peers), daemon=True)
    t1.start()
    t2.start()
    print("Discovery running. Press Ctrl+C to exit.")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
