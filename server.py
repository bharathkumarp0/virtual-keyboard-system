from flask import Flask, jsonify, render_template
import subprocess
import os
import sys

app = Flask(__name__, template_folder="templates")

process = None

@app.route('/')  # Serve index.html on the root URL
def home():
    return render_template("index.html")

@app.route('/start-typing', methods=['GET'])
def start_typing():
    global process
    try:
        if process is None:
            python_executable = sys.executable
            process = subprocess.Popen([python_executable, "main.py"], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ main.py started successfully")
            return jsonify({"message": "Virtual Keyboard Started"}), 200
        else:
            print("⚠️ Virtual Keyboard is already running.")
            return jsonify({"message": "Virtual Keyboard is already running"}), 200
    except Exception as e:
        print("❌ Error starting main.py:", str(e))
        return jsonify({"error": str(e)}), 500
@app.route('/stop-typing', methods=['GET'])
def stop_typing():
    global process
    if process:
        try:
            process.terminate()
            process = None
            return jsonify({"message": "Virtual Keyboard Stopped"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No active process found"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(host='0.0.0.0', port=port, debug=True)
