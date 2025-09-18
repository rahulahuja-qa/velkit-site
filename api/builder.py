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
        return jsonify({"ok": True, "service": "builder"}), 200

    # POST
    d = request.get_json(force=True, silent=True) or {}
    payload = {
        "candidate": {
            "name": str(d.get("name", "")).strip(),
            "contact": str(d.get("contact", "")).strip(),
            "role": str(d.get("role", "")).strip(),
            "years": int(d.get("years_exp") or 0),
            "skills": d.get("skills") or [],
        },
        "job_description": str(d.get("job_description", "")).strip(),
    }
    system = (
        "You are a resume & cover letter builder. Tailor to the job description. "
        "Return ONLY JSON: {cover_letter:string, resume:{summary:string,"
        "experience:[{title,company,bullets[]}], skills:[string]}}"
    )
    result = ask_json(system, payload)
    resp = jsonify(result)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
