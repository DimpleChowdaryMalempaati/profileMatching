# Profile Matching RAG System

A resume retrieval and job-matching system built with **RAG** (Retrieval-Augmented Generation) principles: document chunking, embeddings, vector search, and hybrid ranking.

## Features

### Part A — `resume_rag.py`
- Load resumes via Milestone 1 file-system tools (`.txt`, `.md`, `.pdf`, `.docx`)
- Section-aware chunking (Experience, Education, Skills, etc.)
- Embeddings via **ChromaDB ONNX** (default), **SentenceTransformers**, or **OpenAI**
- Vector storage in **ChromaDB**
- Metadata extraction: Name, Skills, Experience Years, Education

### Part B — `job_matcher.py`
- Semantic search over indexed resumes (top-K=10)
- Hybrid search: semantic similarity + keyword overlap for critical skills
- Scoring on 0–100 scale with match reasoning
- Must-have requirement filtering (e.g., "5+ years Python")

## Quick Start

### Windows (recommended — no venv activation needed)

```powershell
cd D:\D\profileMatching

# 1. Create virtual environment (first time only)
python -m venv .venv

# 2. Install dependencies (first time only)
.venv\Scripts\pip install -r requirements.txt

# 3. Dataset is already included (34 resumes + 6 job descriptions)
#    To regenerate: .venv\Scripts\python main.py generate

# 4. Build vector index
.venv\Scripts\python main.py index --reset

# 5. Match a job
.venv\Scripts\python main.py match --job job_descriptions/senior_python_ml_engineer.json

# 6. Open experimentation notebook
.venv\Scripts\jupyter notebook notebooks/rag_experimentation.ipynb
```

> **Note:** If `.venv\Scripts\activate` fails due to PowerShell policy, always use `.venv\Scripts\python` instead of `python`.

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py index --reset
python main.py match --job job_descriptions/senior_python_ml_engineer.json
jupyter notebook notebooks/rag_experimentation.ipynb
```

## Project Structure

```
profileMatching/
├── tools/
│   └── resume_loader.py    # Milestone 1: load, validate, metadata
├── resume_rag.py           # Chunking, embeddings, ChromaDB
├── job_matcher.py          # Hybrid search & scoring
├── main.py                 # CLI entry point
├── config.py               # Configuration
├── scripts/
│   └── generate_dataset.py # Synthetic dataset generator
├── resumes/                # 34 resume files
├── job_descriptions/       # 6 structured job descriptions
├── notebooks/
│   └── rag_experimentation.ipynb
└── requirements.txt
```

## What each file does

| File | Purpose |
|------|---------|
| `main.py` | CLI — run indexing, matching, list resumes |
| `resume_rag.py` | Chunks resumes, creates embeddings, stores in ChromaDB |
| `job_matcher.py` | Matches job descriptions to resumes (hybrid search + scoring) |
| `tools/resume_loader.py` | Loads/validates resume files, extracts metadata |
| `config.py` | Paths and settings (env vars via `.env`) |
| `scripts/generate_dataset.py` | Creates synthetic resumes and job descriptions |
| `notebooks/rag_experimentation.ipynb` | Accuracy/latency experiments and charts |

## Output Format

```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "John Doe",
      "resume_path": "resumes/john_doe.txt",
      "match_score": 92,
      "matched_skills": ["Python", "Machine Learning"],
      "relevant_excerpts": ["..."],
      "reasoning": "Strong match for ML experience..."
    }
  ]
}
```

## Tool Usage Examples (for LLM agents)

All file-system tools return a consistent envelope: `{success, tool, ...}` or `{success, error}`.

```python
from tools.resume_loader import list_resumes, load_resume, validate_file

# Validate before loading
v = validate_file("resumes/alice_smith.txt")
if v["valid"]:
    doc = load_resume(v["path"])
    print(doc["document"]["metadata"]["name"])

# Batch load
from tools.resume_loader import load_all_resumes
batch = load_all_resumes("resumes")
print(batch["loaded_count"], "resumes loaded")
```

```python
from resume_rag import ResumeRAG

rag = ResumeRAG()
rag.index_resumes("resumes")
results = rag.query("Python machine learning engineer", top_k=5)
```

```python
from job_matcher import JobMatcher

matcher = JobMatcher()
result = matcher.match_job_file("job_descriptions/senior_python_ml_engineer.json")
print(result["top_matches"][0]["match_score"])
```

## Configuration

Copy `.env.example` to `.env`:

```env
EMBEDDING_PROVIDER=chroma
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=data/chroma_db
```

For OpenAI embeddings:
```env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Jupyter Notebook

Open `notebooks/rag_experimentation.ipynb` for:
- Indexing pipeline walkthrough
- Retrieval accuracy evaluation
- Latency benchmarks
- Hybrid vs semantic-only comparison

## Performance Notes

- First run downloads the ONNX embedding model (~90MB)
- Indexing 34 resumes: ~5–15 seconds (CPU)
- Single job match query: ~0.5–2 seconds

## License

MIT — for educational assignment use.
