import time
import threading
import requests
from flask import Flask, render_template_string

# Initialize Flask app
app = Flask(__name__)

# List of websites to monitor
websites = [
    "https://example.com",
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://amazon.com"
]

# Status dictionary
status = {site: "Unknown" for site in websites}

# Website checking function
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
        time.sleep(30)  # Recheck every 30 seconds

# Route for dashboard
@app.route("/")
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Website Uptime Monitor</title>
        <meta http-equiv="refresh" content="15"> <!-- Auto-refresh every 15 seconds -->
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; }
            table { width: 60%; margin: auto; border-collapse: collapse; }
            th, td { padding: 12px; text-align: center; border-bottom: 1px solid #ddd; font-size: 18px; }
            th { background-color: #333; color: white; }
            tr:hover { background-color: #f1f1f1; }
            .up { color: green; font-weight: bold; }
            .down { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Website Uptime Monitor</h1>
        <table>
            <thead>
                <tr>
                    <th>Website</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for site, stat in status.items() %}
                <tr>
                    <td>{{ site }}</td>
                    <td class="{{ 'up' if stat == 'UP' else 'down' }}">{{ stat }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html, status=status)

if __name__ == "__main__":
    # Start background thread
    t = threading.Thread(target=check_websites)
    t.daemon = True
    t.start()

    # Start Flask app
    app.run(host="0.0.0.0", port=5000)

