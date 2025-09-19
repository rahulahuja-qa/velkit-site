from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi, io, json
from api._lib.parsers import read_text_from_upload
from api._lib.ai_client import ask_json
from api._lib.docx_utils import docx_from_review

def _cors(s):
    s.send_header("Access-Control-Allow-Origin", "*")
    s.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    s.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

class _UploadShim:
    # Mimic Flask upload object consumed by read_text_from_upload()
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self._data = data
        self.stream = io.BytesIO(data)
    def read(self): return self._data

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204); _cors(self); self.end_headers()

    def do_GET(self):
        self.send_response(200); _cors(self)
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"ok": true, "service": "review"}')

    def do_POST(self):
        ctype = self.headers.get("Content-Type","")
        if not ctype.startswith("multipart/form-data"):
            self.send_response(400); _cors(self)
            self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(b'{"error":"multipart form required"}'); return

        fs = cgi.FieldStorage(
            fp=self.rfile, headers=self.headers,
            environ={"REQUEST_METHOD":"POST", "CONTENT_TYPE": ctype}
        )
        jd = fs.getfirst("job_description","").strip()
        fileitem = fs["resume"] if "resume" in fs else None
        if not jd or not fileitem or not fileitem.file:
            self.send_response(400); _cors(self)
            self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(b'{"error":"resume and job_description required"}'); return

        filename = getattr(fileitem, "filename", "upload.pdf") or "upload.bin"
        data = fileitem.file.read()
        resume_text = read_text_from_upload(_UploadShim(filename, data))

        system = ("You are a resume reviewer. Compare resume to job description. "
                  "Return ONLY JSON: {ats_score:int, missing_keywords:[string], "
                  "section_feedback:{Summary,Experience,Skills,Education}, "
                  "rewrite_suggestions:[string]}")
        result = ask_json(system, {"job_description": jd, "resume_text": resume_text})

        qs = parse_qs(urlparse(self.path).query)
        want_docx = (qs.get("format", ["json"])[0] == "docx")

        if want_docx and not result.get("error"):
            data = docx_from_review(result)
            self.send_response(200); _cors(self)
            self.send_header("Content-Type",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", 'attachment; filename="velkit-review.docx"')
            self.end_headers()
            self.wfile.write(data); return

        out = json.dumps(result).encode("utf-8")
        self.send_response(200); _cors(self)
        self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(out)
