import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify, make_response
from _lib.parsers import read_text_from_upload
from _lib.scoring import score_resume_vs_jd
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
        return jsonify({"ok": True, "service": "review"}), 200

    jd = request.form.get("job_description", "").strip()
    fs = request.files.get("resume")
    if not jd or not fs:
        return jsonify({"error": "resume and job_description required"}), 400

    resume_text = read_text_from_upload(fs)
    ats_score, _ = score_resume_vs_jd(resume_text, jd)

    system = (
        "You are a resume reviewer. Compare resume to job description. "
        "Return ONLY JSON: {section_feedback:{Summary,Experience,Skills,Education}, "
        "rewrite_suggestions:[string], missing_keywords:[string]}"
    )
    llm = ask_json(system, {"job_description": jd, "resume_text": resume_text})
    payload = {
        "ats_score": ats_score,
        "missing_keywords": llm.get("missing_keywords") or [],
        "section_feedback": llm.get("section_feedback"),
        "rewrite_suggestions": llm.get("rewrite_suggestions"),
    }
    resp = jsonify(payload)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
