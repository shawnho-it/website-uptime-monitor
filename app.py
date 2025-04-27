from flask import Flask, jsonify, render_template_string
import threading
import time
import requests

app = Flask(__name__)

# List of websites to monitor
websites = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.github.com",
    "https://www.amazon.com",
    "https://www.stackoverflow.com"
]

# Website status dictionary
status = {}

def check_websites():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    while True:
        for site in websites:
            try:
                response = requests.get(site, headers=headers, timeout=5, allow_redirects=True)
                if response.status_code in [200, 301, 302]:
                    status[site] = "UP"
                else:
                    status[site] = "DOWN"
            except requests.RequestException:
                status[site] = "DOWN"
        time.sleep(60)  # Check every 60 seconds

# Start the background thread
threading.Thread(target=check_websites, daemon=True).start()

@app.route('/')
def home():
    return "Website Uptime Monitor Running."

@app.route('/status')
def get_status_json():
    return jsonify(status)

@app.route('/dashboard')
def dashboard():
    html_template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta http-equiv="refresh" content="60">
        <title>Website Uptime Monitor Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            .up { color: green; font-weight: bold; }
            .down { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🌐 Website Uptime Monitor</h1>
        <table>
            <tr>
                <th>Website</th>
                <th>Status</th>
            </tr>
            {% for site, state in status.items() %}
            <tr>
                <td>{{ site }}</td>
                <td class="{{ state|lower }}">{{ state }}</td>
            </tr>
            {% endfor %}
        </table>
        <p><i>Auto-refreshes every 60 seconds</i></p>
    </body>
    </html>
    """
    return render_template_string(html_template, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

