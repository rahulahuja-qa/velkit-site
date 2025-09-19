from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from api._lib.ai_client import ask_json
from api._lib.docx_utils import docx_from_builder

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
        self.wfile.write(b'{"ok": true, "service": "builder"}')

    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            d = json.loads(raw) if raw else {}
        except Exception:
            d = {}

        payload = {
            "candidate": {
                "name": str(d.get("name","")).strip(),
                "contact": str(d.get("contact","")).strip(),
                "role": str(d.get("role","")).strip(),
                "years": int(d.get("years_exp") or 0),
                "skills": d.get("skills") or [],
            },
            "job_description": str(d.get("job_description","")).strip(),
        }
        system = ("You are a resume & cover letter builder. Tailor to the job. "
                  "Return ONLY JSON: {cover_letter:string, resume:{summary:string,"
                  "experience:[{title,company,bullets[]}], skills:[string]}}")

        result = ask_json(system, payload)

        qs = parse_qs(urlparse(self.path).query)
        want_docx = (qs.get("format", ["json"])[0] == "docx")

        if want_docx and not result.get("error"):
            data = docx_from_builder(result.get("cover_letter",""), result.get("resume") or {})
            self.send_response(200); _cors(self)
            self.send_header("Content-Type",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", 'attachment; filename="velkit-builder.docx"')
            self.end_headers()
            self.wfile.write(data)
            return

        out = json.dumps(result).encode("utf-8")
        self.send_response(200); _cors(self)
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(out)
