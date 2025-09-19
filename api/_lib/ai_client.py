import os, json
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def ask_json(system_prompt: str, payload: dict) -> dict:
    """Ask Gemini and return parsed JSON or an error dict."""
    prompt = (
        f"{system_prompt}\n\nINPUT JSON:\n{json.dumps(payload)}\n\n"
        "Return ONLY valid JSON. No markdown."
    )
    resp = genai.GenerativeModel(MODEL).generate_content(prompt)
    text = (resp.text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        return {"error": "model did not return JSON", "raw": text[:4000]}