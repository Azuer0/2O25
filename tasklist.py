from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def main():
  return "<h1>Welcome!</h1>"

@app.route('/process_json', methods=['POST'])
def process_json_data():
    start_time = time.time()
    if not request.is_json:
        return jsonify({"wrong": "You need to use json"}), 400

    data = request.het_json()

    end_time = time.time()
    processing_time = (end_time - start_time) * 1000

    response_data = {
        "status": "success",
        "recived_data": data,
        "processing_time": round(processing_time, 2)
    }
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
