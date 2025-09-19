from flask import Flask, request, jsonify, make_response, send_file
from io import BytesIO
from api._lib.ai_client import ask_json
from api._lib.docx_utils import docx_from_builder

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def handle():
    if request.method == "OPTIONS":
        return _preflight()
    if request.method == "GET":
        return jsonify({"ok": True, "service": "builder"})

    d = request.get_json(force=True, silent=True) or {}
    payload = {
        "candidate": {
            "name": str(d.get("name","")).strip(),
            "contact": str(d.get("contact","")).strip(),
            "role": str(d.get("role","")).strip(),
            "years": int(d.get("years_exp") or 0),
            "skills": d.get("skills") or []
        },
        "job_description": str(d.get("job_description","")).strip()
    }
    sys = ("You are a resume & cover letter builder. Tailor to the job. "
           "Return ONLY JSON: {cover_letter:string, resume:{summary:string,"
           "experience:[{title,company,bullets[]}], skills:[string]}}")
    result = ask_json(sys, payload)

    if request.args.get("format") == "docx" and not result.get("error"):
        data = docx_from_builder(result.get("cover_letter",""), result.get("resume") or {})
        return _docx(data, "velkit-builder.docx")

    r = jsonify(result); r.headers["Access-Control-Allow-Origin"] = "*"; return r

def _preflight():
    r = make_response("", 204)
    r.headers["Access-Control-Allow-Origin"]  = "*"
    r.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return r

def _docx(data: bytes, filename: str):
    bio = BytesIO(data); bio.seek(0)
    return send_file(bio,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True, download_name=filename)
