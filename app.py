import time
import threading
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

websites = [
    "https://example.com",
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://amazon.com"
]

status = {site: "Checking..." for site in websites}

def update_status():
    global status
    while True:
        for site in websites:
            try:
                r = requests.get(site, timeout=5)
                if r.status_code in [200, 301, 302]:
                    status[site] = "🟢 UP"
                else:
                    status[site] = "🔴 DOWN"
            except:
                status[site] = "🔴 DOWN"
        time.sleep(10)

@app.route("/")
def dashboard():
    page = """
    <html>
    <head>
        <title>Website Monitor</title>
        <meta http-equiv="refresh" content="15">
        <style>
            body { font-family: Arial; background-color: #f4f4f4; }
            h1 { text-align: center; }
            table { margin: auto; border-collapse: collapse; width: 70%; }
            th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: center; font-size: 18px; }
            th { background-color: #222; color: white; }
            td { background-color: white; }
        </style>
    </head>
    <body>
        <h1>Website Uptime Monitor</h1>
        <table>
            <tr><th>Website</th><th>Status</th></tr>
            {% for site, stat in status.items() %}
            <tr>
                <td>{{ site }}</td>
                <td>{{ stat }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(page, status=status)

if __name__ == "__main__":
    t = threading.Thread(target=update_status)
    t.start()
    app.run(host="0.0.0.0", port=5000)

