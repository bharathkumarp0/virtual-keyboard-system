from flask import Flask, jsonify
import subprocess
import os
import sys
import signal

app = Flask(__name__)

# Store process information globally
process = None

@app.route('/start-typing', methods=['GET'])
def start_typing():
    global process
    try:
        if process is None:  # Ensure only one instance runs
            python_executable = sys.executable
            process = subprocess.Popen([python_executable, os.path.abspath("main.py")], 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return jsonify({"message": "Virtual Keyboard Started"}), 200
        else:
            return jsonify({"message": "Virtual Keyboard is already running"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop-typing', methods=['GET'])
def stop_typing():
    global process
    if process:
        try:
            # Kill the process and all child processes
            os.kill(process.pid, signal.SIGTERM)  # Forcefully stop the process
            process = None  # Reset process variable
            return jsonify({"message": "Virtual Keyboard Stopped"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No active process found"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
