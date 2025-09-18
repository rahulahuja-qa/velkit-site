import re
from textstat import flesch_reading_ease

BANDS = [(80, "Great"), (60, "Good"), (0, "Average")]

def score_resume_vs_jd(resume: str, jd: str):
  r = set(w.lower() for w in re.findall(r"[A-Za-z]{4,}", resume))
  j = set(w.lower() for w in re.findall(r"[A-Za-z]{4,}", jd))
  overlap = len(r & j)
  richness = len(r)
  readability = max(0, min(100, int(flesch_reading_ease(resume))))
  score = min(100, int(0.6 * min(60, overlap) + 0.2 * min(40, richness / 10) + 0.2 * readability))
  for thr, band in BANDS:
    if score >= thr:
      return score, band
  return score, "Average"
