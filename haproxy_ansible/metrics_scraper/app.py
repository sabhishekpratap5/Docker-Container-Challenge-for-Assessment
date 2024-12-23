from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        'cpu_percent': psutil.cpu_percent(),
        'memory': psutil.virtual_memory()._asdict()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
