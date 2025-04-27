from flask import Flask, jsonify
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
    while True:
        for site in websites:
            try:
                response = requests.get(site, timeout=5)
                status[site] = "UP" if response.status_code == 200 else "DOWN"
            except requests.RequestException:
                status[site] = "DOWN"
        time.sleep(60)  # wait 1 minute before checking again

# Start background thread
threading.Thread(target=check_websites, daemon=True).start()

@app.route('/')
def home():
    return "Website Uptime Monitor Running."

@app.route('/status')
def get_status():
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

