# Velkit Site (Flask + HTML + JS on Vercel)

## Structure
- `public/` serves the 4 pages at `/`, `/builder.html`, `/review.html`, `/trainings.html`.
- `api/` provides Python (Flask) endpoints at `/api/builder`, `/api/review`, `/api/trainings`.
- No Next.js. No TSX.

## Environment
Set `GEMINI_API_KEY` in Vercel Project → Settings → Environment Variables.

## Local test (optional)
Create a virtualenv and run any endpoint locally:
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_KEY
# Run one function manually
python - <<'PY'
from api.builder.index import app
app.run(port=5001)
PY
# Visit http://localhost:5001/