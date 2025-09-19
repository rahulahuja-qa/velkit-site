from flask import Flask, request, jsonify, make_response, send_file
from api._lib.parsers import read_text_from_upload
from api._lib.ai_client import ask_json
from api._lib.docx_utils import docx_from_review
from io import BytesIO


app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def handle():
    if request.method == "OPTIONS":
        return _preflight()
    if request.method == "GET":
        return jsonify({"ok": True, "service": "review"})

    jd = request.form.get("job_description","").strip()
    fs = request.files.get("resume")
    if not jd or not fs:
        return jsonify({"error":"resume and job_description required"}), 400

    resume_text = read_text_from_upload(fs)

    sys = ("You are a resume reviewer. Compare resume to job description. "
           "Return ONLY JSON: {ats_score:int, missing_keywords:[string], "
           "section_feedback:{Summary,Experience,Skills,Education}, "
           "rewrite_suggestions:[string]}")
    result = ask_json(sys, {"job_description": jd, "resume_text": resume_text})

    if request.args.get("format") == "docx" and not result.get("error"):
        data = docx_from_review(result)
        return _docx(data, "velkit-review.docx")

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
