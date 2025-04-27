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

# Status dictionary to keep track of website statuses
status = {site: "Unknown" for site in websites}

# Function to check the websites' statuses
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
        time.sleep(60)  # Wait 60 seconds before checking again

# Flask route for dashboard
@app.route("/")
def dashboard():
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <title>Website Uptime Monitor</title>
        <meta http-equiv="refresh" content="30">  <!-- Auto refresh page every 30 seconds -->
    </head>
    <body>
        <h1>Website Uptime Status</h1>
        <table border="1" cellpadding="10" cellspacing="0">
            <tr>
                <th>Website</th>
                <th>Status</th>
            </tr>
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
    return render_template_string(html, status=status)

if __name__ == "__main__":
    # Start background thread for checking websites
    t = threading.Thread(target=check_websites)
    t.daemon = True
    t.start()
    # Start Flask server
    app.run(host="0.0.0.0", port=5000)

