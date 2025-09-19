from flask import Flask, request, jsonify, make_response, send_file
from _lib.ai_client import ask_json
from _lib.docx_utils import docx_from_trainings
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def handle():
    if request.method == "OPTIONS":
        return _preflight()
    if request.method == "GET":
        return jsonify({"ok": True, "service": "trainings"})

    d = request.get_json(force=True, silent=True) or {}
    payload = {
        "target_role": str(d.get("target_role","")).strip(),
        "current_skills": d.get("current_skills") or [],
        "interests": d.get("interests") or []
    }
    sys = ("Recommend a staged plan. Return ONLY JSON: "
           "{plan:[{title,provider,level,why,estimated_hours:int}]} "
           "Use reputable providers (edX, Coursera, Google, AWS, Azure, PMI, etc.)")
    result = ask_json(sys, payload)

    if request.args.get("format") == "docx" and not result.get("error"):
        data = docx_from_trainings(result.get("plan") or [])
        return _docx(data, "velkit-trainings.docx")

    resp = jsonify(result)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

def _preflight():
    r = make_response("", 204)
    r.headers["Access-Control-Allow-Origin"]  = "*"
    r.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return r

def _docx(data: bytes, filename: str):
    bio = BytesIO(data); bio.seek(0)
    return send_file(
        bio,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=filename
    )
