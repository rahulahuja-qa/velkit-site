from flask import Flask, request, jsonify, make_response
from _lib.ai_client import ask_json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def handle():
    if request.method == "OPTIONS":
        resp = make_response("", 204)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return resp

    if request.method == "GET":
        return jsonify({"ok": True, "service": "trainings"}), 200

    # POST
    d = request.get_json(force=True, silent=True) or {}
    payload = {
        "target_role": str(d.get("target_role", "")).strip(),
        "current_skills": d.get("current_skills") or [],
        "interests": d.get("interests") or [],
    }
    system = (
        "Recommend a staged plan. Return ONLY JSON: "
        "{plan:[{title,provider,level,why,estimated_hours:int}]}. "
        "Use reputable providers (edX, Coursera, Google, AWS, Azure, PMI, etc.)"
    )
    result = ask_json(system, payload)
    resp = jsonify(result)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
