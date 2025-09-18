from flask import Flask, request, jsonify
from _lib.ai_client import ask_json

app = Flask(__name__)

@app.post("/")
def trainings():
  d = request.get_json(force=True, silent=True) or {}
  payload = {
    "target_role": str(d.get("target_role","")).strip(),
    "current_skills": d.get("current_skills") or [],
    "interests": d.get("interests") or []
  }
  system = (
    "Recommend a staged plan. Return ONLY JSON: "
    "{plan:[{title,provider,level,why,estimated_hours:int}]}. "
    "Use reputable providers (edX, Coursera, Google, AWS, Azure, PMI, etc.)"
  )
  return jsonify(ask_json(system, payload))
