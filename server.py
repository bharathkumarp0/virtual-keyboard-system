from flask import Flask, jsonify, render_template
import subprocess
import os
import sys

app = Flask(__name__, template_folder="templates")

process = None

@app.route('/')  # Ensure the root URL is mapped to index.html
def home():
    return render_template("index.html")

@app.route('/start-typing', methods=['GET'])
def start_typing():
    global process
    if process is None:
        python_executable = sys.executable
        process = subprocess.Popen([python_executable, os.path.abspath("main.py")])
        return jsonify({"message": "Virtual Keyboard Started"}), 200
    else:
        return jsonify({"message": "Virtual Keyboard is already running"}), 200

@app.route('/stop-typing', methods=['GET'])
def stop_typing():
    global process
    if process:
        process.terminate()
        process = None
        return jsonify({"message": "Virtual Keyboard Stopped"}), 200
    return jsonify({"error": "No active process found"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Ensure it uses the assigned Render port
    app.run(host='0.0.0.0', port=port, debug=True)


