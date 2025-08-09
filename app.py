#!/usr/bin/env python3
from flask import Flask, send_from_directory, request, jsonify, abort
from pathlib import Path
import json

APP_DIR = Path(__file__).parent.resolve()
PRESETS_PATH = APP_DIR / "presets.json"

app = Flask(__name__, static_folder=str(APP_DIR), static_url_path="")

@app.get("/")
def root():
    return send_from_directory(str(APP_DIR), "index.html")

@app.get("/api/presets")
def get_presets():
    if not PRESETS_PATH.exists():
        return jsonify({"banks": []})
    try:
        with PRESETS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "banks" not in data:
            data = {"banks": []}
        return jsonify(data)
    except Exception as e:
        abort(500, f"Failed to read presets.json: {e}")

@app.put("/api/presets")
def put_presets():
    try:
        data = request.get_json(force=True, silent=False)
        if not isinstance(data, dict) or "banks" not in data or not isinstance(data["banks"], list):
            abort(400, "Payload must be an object with a 'banks' array.")
        tmp = PRESETS_PATH.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(PRESETS_PATH)
        return jsonify({"ok": True})
    except Exception as e:
        abort(500, f"Failed to write presets.json: {e}")

if __name__ == "__main__":
    # pip install flask
    app.run(host="127.0.0.1", port=5000, debug=True)
