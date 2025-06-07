import threading
import time
import requests
import socket
import subprocess
import json
import os
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

# ==== Flask Server Section ====
app = Flask(__name__)
status_data = {}
SERVER_PORT = 5000
DISCOVERY_FILE = "/tmp/mesh_peers.json"

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mesh Node Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: sans-serif; background: #fafafa; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #eee; }
        .hostname { font-weight: bold; }
        pre { font-size: 0.95em; margin: 0; }
    </style>
</head>
<body>
    <h1>Mesh Node Dashboard</h1>
    <table>
        <tr>
            <th>Hostname</th>
            <th>IP</th>
            <th>Last Updated</th>
            <th>Neighbors</th>
            <th>Uptime</th>
        </tr>
        {% for host, data in status_data.items() %}
        <tr>
            <td class="hostname">{{host}}</td>
            <td>{{data['ip']}}</td>
            <td>{{data['time']}}</td>
            <td><pre>{{data['info'].get('batman_neighbors','')}}</pre></td>
            <td><pre>{{data['info'].get('uptime','')}}</pre></td>
        </tr>
        {% endfor %}
    </table>
    <p>Auto-refresh every 5 seconds.</p>
</body>
</html>
"""

@app.route('/status', methods=['POST'])
def receive_status():
    data = request.get_json()
    hostname = data.get('hostname', 'unknown')
    status_data[hostname] = {
        "ip": data.get('ip'),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "info": data.get('info', {})
    }
    return jsonify({"result": "success"})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(status_data)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, status_data=status_data)

def run_flask():
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=False, use_reloader=False)

# ==== Status Sending Section ====
def get_ip():
    try:
        result = subprocess.check_output("hostname -I", shell=True)
        return result.decode().strip().split()[0]
    except Exception:
        return None

def get_peers():
    peers = set()
    if os.path.exists(DISCOVERY_FILE):
        with open(DISCOVERY_FILE) as f:
            try:
                data = json.load(f)
                peers = set(data.keys())
            except Exception:
                pass
    return peers

def send_status_periodically(interval=30):
    hostname = socket.gethostname()
    while True:
        ip = get_ip()
        info = {
            "batman_neighbors": subprocess.getoutput("batctl n"),
            "uptime": subprocess.getoutput("uptime"),
        }
        data = {
            "hostname": hostname,
            "ip": ip,
            "info": info
        }
        peers = get_peers()
        # Always send to self too!
        if ip:
            peers.add(ip)
        for peer_ip in peers:
            url = f"http://{peer_ip}:{SERVER_PORT}/status"
            try:
                r = requests.post(url, json=data, timeout=3)
                print(f"Status sent to {url}: {r.status_code}")
            except Exception as e:
                print(f"Failed to send status to {url}: {e}")
        time.sleep(interval)

# ==== Main Entrypoint ====
if __name__ == "__main__":
    # Start Flask server in a thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("Flask dashboard running.")

    # Start status sending loop (main thread)
    send_status_periodically(interval=30)
