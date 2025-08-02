from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store latest status
latest_status = {
    'keyword': None,
    'transcription': None,
    'response': None,
    'response_type': None,
    'timestamp': None
}

@app.route('/keyword_detected', methods=['POST'])
def keyword_detected():
    data = request.json
    latest_status['keyword'] = data['keyword']
    latest_status['timestamp'] = data['timestamp']
    return jsonify({"status": "success"}), 200

@app.route('/transcription', methods=['POST'])
def transcription():
    data = request.json
    latest_status['transcription'] = data['transcription']
    latest_status['timestamp'] = data['timestamp']
    return jsonify({"status": "success"}), 200

@app.route('/assistant_response', methods=['POST'])
def assistant_response():
    data = request.json
    latest_status['response'] = data['response']
    latest_status['response_type'] = data['response_type']
    latest_status['timestamp'] = data['timestamp']
    return jsonify({"status": "success"}), 200

@app.route('/reset', methods=['POST'])
def reset_status():
    global latest_status
    latest_status = {
        'keyword': None,
        'transcription': None,
        'response': None,
        'response_type': None,
        'timestamp': None
    }
    return jsonify({"status": "reset successful"}), 200

@app.route('/get_latest_status', methods=['GET'])
def get_latest_status():
    return jsonify(latest_status)

if __name__ == '__main__':
    app.run(debug=True)