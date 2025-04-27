from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
checks = []

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

@app.route('/check', methods=['POST'])
def check_website():
    data = request.get_json()
    url = data.get('url')

    try:
        response = requests.get(url, timeout=5)
        status = 'UP' if response.status_code == 200 else 'DOWN'
    except Exception:
        status = 'DOWN'

    check_result = {
        'url': url,
        'status': status
    }
    checks.append(check_result)

    return jsonify(check_result), 200

@app.route('/checks', methods=['GET'])
def get_checks():
    return jsonify(checks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

