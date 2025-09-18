import json
from flask import Flask, request, jsonify
from _lib.ai_client import ask_json

app = Flask(__name__)

@app.post("/")
def build():
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
  system = (
    "You are a resume & cover letter builder. Tailor to the job description. "
    "Return ONLY JSON: {cover_letter:string, resume:{summary:string, "
    "experience:[{title,company,bullets[]}], skills:[string]}}"
  )
  return jsonify(ask_json(system, payload))
