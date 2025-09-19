from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from api._lib.ai_client import ask_json
from api._lib.docx_utils import docx_from_trainings

def _cors(s):
    s.send_header("Access-Control-Allow-Origin", "*")
    s.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    s.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204); _cors(self); self.end_headers()

    def do_GET(self):
        self.send_response(200); _cors(self)
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"ok": true, "service": "trainings"}')

    def do_POST(self):
        length = int(self.headers.get("content-length","0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            d = json.loads(raw) if raw else {}
        except Exception:
            d = {}
        payload = {
            "target_role": str(d.get("target_role","")).strip(),
            "current_skills": d.get("current_skills") or [],
            "interests": d.get("interests") or [],
        }
        system = ("Recommend a staged plan. Return ONLY JSON: "
                  "{plan:[{title,provider,level,why,estimated_hours:int}]}. "
                  "Use reputable providers (edX, Coursera, Google, AWS, Azure, PMI, etc.)")
        result = ask_json(system, payload)

        qs = parse_qs(urlparse(self.path).query)
        want_docx = (qs.get("format", ["json"])[0] == "docx")

        if want_docx and not result.get("error"):
            data = docx_from_trainings(result.get("plan") or [])
            self.send_response(200); _cors(self)
            self.send_header("Content-Type",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", 'attachment; filename="velkit-trainings.docx"')
            self.end_headers()
            self.wfile.write(data); return

        out = json.dumps(result).encode("utf-8")
        self.send_response(200); _cors(self)
        self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(out)
