# Demo Video Script (3–4 minutes)

Use this script to record your assignment demo. Tools: OBS Studio, Windows Game Bar (Win+G), or Loom.

---

## 0:00 – 0:30 | Introduction

**Say:**
> "Hi, I'm [Your Name]. This is my Profile Matching RAG project. It indexes resumes into a vector database and matches candidates to job descriptions using semantic search plus keyword hybrid ranking."

**Show:** Project folder in VS Code / Cursor with `resume_rag.py`, `job_matcher.py`, `tools/resume_loader.py`.

---

## 0:30 – 1:15 | Setup & Dataset

**Terminal commands (run live or pre-recorded):**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py generate
python main.py list
```

**Say:**
> "I generated 34 diverse resumes and 6 job descriptions. The resume loader validates file types and extracts metadata like name, skills, experience years, and education."

**Show:** One resume file open + output of `python main.py list`.

---

## 1:15 – 2:00 | Build RAG Index

```bash
python main.py index --reset
python main.py stats
```

**Say:**
> "The RAG pipeline chunks resumes by section—Experience, Education, Skills—embeds them with HuggingFace sentence-transformers, and stores vectors in ChromaDB with metadata for filtering."

**Show:** JSON output with `chunks_indexed` and `latency_seconds`.

---

## 2:00 – 2:45 | Job Matching

```bash
python main.py match --job job_descriptions/senior_python_ml_engineer.json
```

**Say:**
> "For this Senior Python ML Engineer role, the matcher retrieves top-10 candidates. It combines semantic similarity with keyword matching for critical skills, scores 0–100, and explains which sections matched. Must-have filters like 5+ years Python are enforced."

**Show:** Scroll through `top_matches` — highlight `match_score`, `matched_skills`, `reasoning`.

Optional:
```bash
python main.py match --all --output results/all_matches.json
```

---

## 2:45 – 3:30 | Notebook & Metrics

**Open:** `notebooks/rag_experimentation.ipynb`

**Say:**
> "The notebook evaluates retrieval accuracy using labeled expected matches, measures query latency, and compares hybrid vs semantic-only search."

**Show:** Cells with accuracy chart and latency table.

---

## 3:30 – 4:00 | Wrap-up

**Say:**
> "The system handles PDF, DOCX, and TXT resumes with consistent error responses. Tool outputs use a standard success/error schema so LLM agents can reliably call list, validate, load, index, and match operations. Code is on GitHub at [your repo URL]. Thanks for watching."

**Show:** GitHub repo page briefly.

---

## Recording Tips

1. Increase terminal font size (16–18pt)
2. Use a clean terminal theme
3. Pre-run `pip install` and first index so the demo isn't waiting on model download
4. Keep mouse movements slow and deliberate
5. Export video as MP4, 1080p if possible

## Submission Checklist

- [ ] GitHub repo pushed with all code
- [ ] 30+ resumes in `resumes/`
- [ ] 5+ job descriptions in `job_descriptions/`
- [ ] Notebook runs end-to-end
- [ ] Demo video uploaded (YouTube unlisted, Google Drive, or attach to submission)
- [ ] README includes repo link and video link
