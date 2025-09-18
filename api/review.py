from flask import Flask, request, jsonify
from _lib.parsers import read_text_from_upload
from _lib.scoring import score_resume_vs_jd
from _lib.ai_client import ask_json

app = Flask(__name__)

@app.post("/")
def review():
  jd = request.form.get("job_description","").strip()
  fs = request.files.get("resume")
  if not jd or not fs:
    return jsonify({"error":"resume and job_description required"}), 400

  resume_text = read_text_from_upload(fs)
  score, band = score_resume_vs_jd(resume_text, jd)

  system = (
    "You are a resume reviewer. Compare resume to job description. "
    "Return ONLY JSON: {section_feedback:{Summary,Experience,Skills,Education}, "
    "rewrite_suggestions:[string]}"
  )
  llm = ask_json(system, {"job_description": jd, "resume_text": resume_text})
  return jsonify({
    "ats_score": score,
    "missing_keywords": llm.get("missing_keywords") or [],
    "section_feedback": llm.get("section_feedback"),
    "rewrite_suggestions": llm.get("rewrite_suggestions")
  })
