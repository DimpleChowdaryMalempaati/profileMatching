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

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset (34 resumes + 6 job descriptions)
python main.py generate

# 4. Build vector index
python main.py index --reset

# 5. Match a job
python main.py match --job job_descriptions/senior_python_ml_engineer.json

# 6. Match all jobs
python main.py match --all --output results/all_matches.json
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
├── DEMO_SCRIPT.md          # 3–4 min demo video script
└── requirements.txt
```

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

## Demo Video

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for a 3–4 minute recording script covering setup, indexing, matching, and notebook metrics.

## Performance Notes

- First run downloads the ONNX embedding model (~90MB)
- Indexing 34 resumes: ~5–15 seconds (CPU)
- Single job match query: ~0.5–2 seconds

## License

MIT — for educational assignment use.
