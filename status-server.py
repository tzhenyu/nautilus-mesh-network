from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
status_data = {}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
